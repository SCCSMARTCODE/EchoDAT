"""
This module contains the class that captures message_info table
    in our database
"""

from model.basemodel import Base, BaseModel
from sqlalchemy import Column, String, INTEGER, ForeignKey, TEXT
from sqlalchemy.orm import relationship


class MessageInfo(BaseModel, Base):
    """
    This is the table class that stores the info of messages
    """
    __tablename__ = 'message_info'

    message_level = Column(INTEGER, nullable=False, default=0)
    rmid = Column(INTEGER, nullable=False, default=0)
    commentToId = Column(String(50), ForeignKey('audio_file_info._id'), default=None)
    message = Column(TEXT(10000), nullable=False)
    creatorId = Column(String(50), ForeignKey('user_info._id'), nullable=False)  # note this
    groupId = Column(String(50), ForeignKey('group_info._id'), default=None)
    projectId = Column(String(50), ForeignKey('project_info._id'), default=None)
    creator = relationship('UserInfo', backref='messages')
    group = relationship('GroupInfo', backref='messages')
    project = relationship('ProjectInfo', backref='messages')
    audio = relationship('AudioFileInfo', backref='comments')
