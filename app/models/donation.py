from sqlalchemy import Integer, Column, ForeignKey, Text

from .abstractclass import AbstractClass

class Donation(AbstractClass):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
