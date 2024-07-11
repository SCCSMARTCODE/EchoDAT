"""
This module contains the class that captures users_info table
    in our database
"""

from model.basemodel import BaseModel, Base
from sqlalchemy import Column, String, INTEGER, BOOLEAN
from flask_login import UserMixin


class UserInfo(BaseModel, Base, UserMixin):
    """
    This is the table class that stores the info of users
    """
    __tablename__ = 'user_info'

    userName = Column(String(70), unique=True, nullable=False)
    emailAddress = Column(String(100), unique=True, nullable=False)
    passWord = Column(String(70), nullable=True, unique=True)
    pictureAvailability = Column(BOOLEAN, default=False)
    totalProjectCount = Column(INTEGER, nullable=False, default=0)

    def get_id(self):
        return str(self._id)
