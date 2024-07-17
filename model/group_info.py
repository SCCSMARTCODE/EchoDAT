"""
This module contains the class that captures groups_info table
    in our database
"""

from model.basemodel import Base, BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class GroupInfo(BaseModel, Base):
    """
    This is the table class that stores the info of group

    """
    __tablename__ = 'group_info'

    name = Column(String(70), nullable=False)
    description = Column(String(1000), nullable=False)
    creatorId = Column(String(50), ForeignKey('user_info._id'), nullable=False)  # Foreign key to user_info
    amountOfMembers = Column(Integer, nullable=False, default=1)
    totalProjectCount = Column(Integer, nullable=False, default=0)
    publishedSongsCount = Column(Integer, nullable=False, default=0)

    # Relationships to other tables
    owner = relationship('UserInfo', backref='groups')

    __table_args__ = (
        UniqueConstraint('_id', name='_id'),
    )



