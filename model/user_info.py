"""
This module contains the class that captures users_info table
    in our database
"""

from model.basemodel import BaseModel, Base
from sqlalchemy import Column, String, Integer, Boolean, Text, UniqueConstraint
from flask_login import UserMixin


class UserInfo(BaseModel, Base, UserMixin):
    """
    This is the table class that stores the info of users
    """
    __tablename__ = 'user_info'

    userName = Column(String(70), unique=True, nullable=False)
    emailAddress = Column(String(100), unique=True, nullable=False)
    passWord = Column(String(70), nullable=True, unique=True)
    pictureAvailability = Column(Boolean, default=False)
    homeTown = Column(String(200), nullable=True)
    location = Column(String(555), nullable=True)
    websiteUrl = Column(String(400), nullable=True)
    shortBiography = Column(Text, nullable=True)
    totalProjectCount = Column(Integer, nullable=False, default=0)
    followers = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint('userName', name='userName'),
        UniqueConstraint('emailAddress', name='emailAddress'),
        UniqueConstraint('_id', name='_id'),
        UniqueConstraint('passWord', name='passWord')
    )

    def get_id(self):
        return str(self._id)
