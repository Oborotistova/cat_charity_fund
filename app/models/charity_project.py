from sqlalchemy import Column, String, Text

from app.models.abstractclass import BaseClass


class CharityProject(BaseClass):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
