"""
This module contains the class that captures groups_registration_info table
    in our database

    this will capture your data when you join any group
"""

from model.basemodel import Base, BaseModel
from sqlalchemy import Column, String, INTEGER, ForeignKey
from sqlalchemy.orm import relationship


class GroupRegistrationInfo(BaseModel, Base):
    """
    This is the table class that stores the info of group registration

    """
    __tablename__ = 'group_registration_info'

    userId = Column(String(50), ForeignKey('user_info._id'), nullable=False)
    groupId = Column(String(50), ForeignKey('group_info._id'), nullable=False)
    user_info = relationship('UserInfo', backref='groups_info')
    group_info = relationship('GroupInfo', backref='users_info')




