"""
This module contains the class that captures message_info table
    in our database
"""

from model.basemodel import Base, BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, Text, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship


class MessageInfo(BaseModel, Base):
    """
    This is the table class that stores the info of messages
    """
    __tablename__ = 'message_info'

    message_level = Column(Integer, nullable=False, default=0)
    rmid = Column(Integer, nullable=False, default=0)
    commentToId = Column(String(50), ForeignKey('audio_file_info._id'), default=None)
    message = Column(Text, nullable=False)
    creatorId = Column(String(50), ForeignKey('user_info._id'), nullable=False)
    groupId = Column(String(50), ForeignKey('group_info._id'), default=None)
    projectId = Column(String(50), ForeignKey('project_info._id'), default=None)

    # Relationships to other tables
    creator = relationship('UserInfo', backref='messages')
    group = relationship('GroupInfo', backref='messages')
    project = relationship('ProjectInfo', backref='messages')
    audio = relationship('AudioFileInfo', backref='comments')

    __table_args__ = (
        UniqueConstraint('_id', name='_id'),
    )
