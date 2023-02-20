from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None,
        max_length=100,
        title='Название проекта',
        description='от 1 до 100 символов включительно')
    description: Optional[str] = Field(
        None,
        title='Описание проекта',
        description='обязательное поле, текст; не менее одного символа')
    full_amount: Optional[PositiveInt] = Field(
        None,
        title='Требуемая сумма',
        description='Целочисленное поле; больше 0')

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectCreate(BaseModel):
    name: str = Field(
        ...,
        max_length=100,
        title='Название проекта',
        description='от 1 до 100 символов включительно')
    description: str = Field(
        ...,
        title='Описание проекта',
        description='обязательное поле, текст; не менее одного символа')
    full_amount: PositiveInt = Field(
        ...,
        title='Требуемая сумма',
        description='Целочисленное поле; больше 0')

    class Config:
        title = 'Класс для создания проекта'
        min_anystr_length = 1
        schema_extra = {
            'example': {
                'name': 'Cats',
                'description': 'Hilfe',
                'full_amount': 200,
            }
        }


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int = Field(
        0,
        title='Внесённая сумма',
        description='Целочисленное поле; значение по умолчанию — 0')
    fully_invested: bool = Field(
        False,
        title='Закрыт ли проект',
        description='Собрана ли нужная сумма для проекта')
    create_date: datetime = Field(
        ...,
        title='Дата создания проекта',
        description='Тип DateTime, добавляется автоматически в момент создания проекта')
    close_date: Optional[datetime] = Field(
        ...,
        title='Дата закрытия проекта',
        description='Тип DateTime, проставляется автоматически в момент набора нужной суммы')

    class Config:
        title = 'Класс для описания проекта, полученного из БД'
        orm_mode = True
        schema_extra = {
            'example': {
                'name': 'Cats',
                'description': 'Hilfe',
                'full_amount': 200,
                'invested_amount': 2,
                'fully_invested': False,
                'create_date': 'Mon,20 Feb 2023 15:23:09 GMT',
                'close_date': ''
            }
        }


class CharityProjectUpdate(CharityProjectBase):
    class Config:
        title = 'Класс для редактирования проекта'
        schema_extra = {
            'example': {
                'name': 'Cats',
                'description': 'Hilfe',
                'full_amount': 200,
            }
        }