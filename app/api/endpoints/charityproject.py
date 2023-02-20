from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_already_invested,
                                check_charity_project_closed,
                                check_charity_project_exists,
                                check_charity_project_invested_sum,
                                check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charityproject_crud
from app.models import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.services import investing_process

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Создать благотворительный проект'
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    await charityproject_crud.get_project_id_by_name(
        charity_project.name, session
    )
    new_project = await charityproject_crud.create(charity_project, session)
    await investing_process(new_project, Donation, session)
    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
    summary='Получить список всех проектов'
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    all_projects = await charityproject_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary='Внести изменения в проект'
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_charity_project_exists(
        project_id, session
    )
    check_charity_project_closed(project)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        check_charity_project_invested_sum(project, obj_in.full_amount)

    charity_project = await charityproject_crud.update(
        project, obj_in, session
    )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary='Удалить проект'
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_charity_project_exists(
        project_id, session
    )
    check_charity_project_already_invested(project)
    charity_project = await charityproject_crud.remove(
        project, session
    )
    return charity_project
