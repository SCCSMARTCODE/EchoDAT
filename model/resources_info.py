"""
This module contains the class that captures resources_info table
    in our database
"""

from model.basemodel import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship


class ResourcesInfo(BaseModel, Base):
    """
    This is the table class that stores the info of resources files
    """
    __tablename__ = 'resources_info'

    title = Column(String(60), nullable=False)
    caption = Column(String(1200), nullable=False)
    resourcesType = Column(String(60), nullable=False)
    creatorId = Column(String(50), ForeignKey('user_info._id'), nullable=False)  # Foreign key to user_info
    groupId = Column(String(50), ForeignKey('group_info._id'), nullable=True)  # Foreign key to group_info
    projectId = Column(String(50), ForeignKey('project_info._id'), nullable=True)  # Foreign key to project_info

    # Relationships to other tables
    creator = relationship('UserInfo', backref='resources')
    group = relationship('GroupInfo', backref='resources')
    project = relationship('ProjectInfo', backref='resources')

    __table_args__ = (
        UniqueConstraint('_id', name='_id'),
    )
