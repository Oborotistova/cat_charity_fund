from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def close_donation(
        obj_in: Union[CharityProject, Donation]
) -> Union[CharityProject, Donation]:
    obj_in.invested_amount = obj_in.full_amount
    obj_in.fully_invested = True
    obj_in.close_date = datetime.now()
    return obj_in


async def investing_money(
    obj_in: Union[CharityProject, Donation],
    obj_model: Union[CharityProject, Donation],
) -> Union[CharityProject, Donation]:
    free_amount_in = obj_in.full_amount - obj_in.invested_amount
    free_amount_in_model = obj_model.full_amount - obj_model.invested_amount
    if free_amount_in > free_amount_in_model:
        obj_in.invested_amount += free_amount_in_model
        await close_donation(obj_model)
    elif free_amount_in == free_amount_in_model:
        await close_donation(obj_in)
        await close_donation(obj_model)
    else:
        obj_model.invested_amount += free_amount_in
        await close_donation(obj_in)
    return obj_in, obj_model


async def investing_process(
    obj_in: Union[CharityProject, Donation],
    model_add: Union[CharityProject, Donation],
    session: AsyncSession,
) -> Union[CharityProject, Donation]:
    objects = await session.execute(
        select(model_add).where(model_add.fully_invested == 0
                                ).order_by(model_add.create_date))
    invested_objects = objects.scalars().all()
    for inv in invested_objects:
        obj_in, inv = await investing_money(obj_in, inv)
        session.add(obj_in)
        session.add(inv)
    await session.commit()
    await session.refresh(obj_in)
    return obj_in
