from sqlalchemy import Column, String, Text

from .abstractclass import AbstractClass


class CharityProject(AbstractClass):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)