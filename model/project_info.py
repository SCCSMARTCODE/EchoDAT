"""
This module contains the class that captures users_info table
    in our database
"""

from model.basemodel import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey, Text, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship


class ProjectInfo(BaseModel, Base):
    """
    This is the table class that stores the info of users
    """
    __tablename__ = 'project_info'

    name = Column(String(70), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    creatorId = Column(String(50), ForeignKey('user_info._id'), nullable=False)
    groupId = Column(String(50), ForeignKey('group_info._id'), nullable=True, default=None)

    creator = relationship('UserInfo', backref='projects')
    group = relationship('GroupInfo', backref='projects')

    __table_args__ = (
        UniqueConstraint('name', name='name'),
        UniqueConstraint('_id', name='_id'),
    )
