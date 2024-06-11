"""
This module contains the class that captures users_info table
    in our database
"""

from model.basemodel import Base, BaseModel
from sqlalchemy import Column, String, INTEGER


class UserInfo(Base, BaseModel):
    """
    This is the table class that stores the info of users
    """
    __tablename__ = 'user_info'

    userName = Column(String(70), unique=True, nullable=False)
    fullName = Column(String(255), nullable=False)
    emailAddress = Column(String(100), unique=True, nullable=False)
    passWord = Column(String(40), nullable=False, unique=True)
    totalProjectCount = Column(INTEGER, nullable=False, default=0)


    
