from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charityproject_crud
from app.models import CharityProject


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charityproject_crud.get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


def check_charity_project_invested_sum(
        project: CharityProject,
        chek_amount: int) -> None:
    if project.invested_amount > chek_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя установить сумму, ниже уже вложенной!'
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> Optional[CharityProject]:
    project = await charityproject_crud.get_charity_project_by_id(
        project_id, session
    )
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return project


def check_charity_project_already_invested(
        charityproject: CharityProject) -> None:
    if charityproject.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


def check_charity_project_closed(
        charityproject: CharityProject) -> None:
    if charityproject.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
