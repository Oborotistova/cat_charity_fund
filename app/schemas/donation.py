from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt = Field(
        ...,
        title='Сумма пожертвования',
        description='Целочисленное поле; больше 0')
    comment: Optional[str] = Field(
        None,
        title='Комментарий',
        description='Необязательное текстовое поле')

    class Config:
        title = 'Класс для создания пожертвования'
        schema_extra = {
            'example': {
                'full_amount': 200,
                'comment': 'comment',
            }
        }


class DonationCreate(DonationBase):
    id: int
    create_date: datetime = Field(
        ...,
        title='Дата пожертвованияа',
        description='Тип DateTime; в момент поступления пожертвования')

    class Config:
        title = 'Класс для описания пожертвования, полученного из БД'
        orm_mode = True
        schema_extra = {
            'example': {
                'full_amount': 200,
                'comment': 'comment',
                'create_date': 'Mon,20 Feb 2023 15:23:09 GMT',
            }
        }


class DonationDB(DonationCreate):
    id: int
    create_date: datetime = Field(
        ...,
        title='Дата пожертвованияа',
        description='Тип DateTime; в момент поступления пожертвования')
    user_id: int = Field(
        ...,
        title='id пользователя, сделавшего пожертвование',
        description='Foreign Key на поле user.id из таблицы пользователей')
    invested_amount: int = Field(
        0,
        title='Cумма из пожертвования, которая распределена по проектам',
        description='Значение по умолчанию равно 0')
    fully_invested: bool = Field(
        False,
        title='Все ли деньги были переведены в тот или иной проект',
        description='Значение по умолчанию равно False')
    close_date: Optional[datetime] = Field(
        ...,
        title='Дата, когда вся сумма была распределена по проектам',
        description='Тип DateTime; в момент выполнения условия')

    class Config:
        title = 'Класс для описания пожертвования полученного из БД, в списке'
        orm_mode = True
        schema_extra = {
            'example': {
                'full_amount': 200,
                'comment': 'comment',
                'create_date': 'Mon,20 Feb 2023 15:23:09 GMT',
                'invested_amount': 2,
                'fully_invested': False,
                'create_date': 'Mon,20 Feb 2023 15:23:09 GMT',
                'close_date': 'Mon,21 Feb 2023 15:23:09 GMT',
            }
        }