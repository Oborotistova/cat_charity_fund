from sqlalchemy import Integer, Column, ForeignKey, Text

from app.models.abstractclass import BaseClass


class Donation(BaseClass):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
