"""
This module contains the class that captures groups_info table
    in our database
"""

from model.basemodel import Base, BaseModel
from sqlalchemy import Column, String, INTEGER, ForeignKey
from sqlalchemy.orm import relationship


class AudioFileInfo(BaseModel, Base):
    """
    This is the table class that stores the info of audio files
    """
    __tablename__ = 'audio_file_info'

    title = Column(String(70), nullable=False)
    artist = Column(String(70), nullable=False)
    featuring = Column(String(70), nullable=False)
    producersName = Column(String(270), nullable=False)
    genre = Column(String(70), nullable=False)
    mood = Column(String(70), nullable=False)
    caption = Column(String(900), nullable=False)
    creatorId = Column(String(50), ForeignKey('user_info._id'), nullable=False)  # note this
    groupId = Column(String(50), ForeignKey('group_info._id'), default=None)
    projectId = Column(String(50), ForeignKey('project_info._id'), nullable=True)
    release = Column(String(20), nullable=False, default='PRIVATE')
    likesCount = Column(INTEGER, nullable=False, default=0)
    framePictureName = Column(String(50), nullable=False, default='default.jpg')
    lyricsIdentityName = Column(String(50))  # plan to store this ia a file in form of a json file one file for a group
    creator = relationship('UserInfo', backref='audios')
    group = relationship('GroupInfo', backref='audios')
    project = relationship('ProjectInfo', backref='audios')
