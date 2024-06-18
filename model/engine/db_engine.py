from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from model.basemodel import Base
from model.user_info import UserInfo
from model.group_info import GroupInfo
from model.message_info import MessageInfo
from model.project_info import ProjectInfo
from model.audio_file_info import AudioFileInfo
from model.group_registration_info import GroupRegistrationInfo


class Storage(object):

    def __init__(self):
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}:{}/{}".format(
            os.getenv('DB_USER'),
            os.getenv('DB_PASSWORD'),
            os.getenv('DB_HOST'),
            os.getenv('DB_PORT'),
            os.getenv('DB_NAME')
        ), echo=True)

        session = sessionmaker(self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()
        Base.metadata.create_all(self.__engine)

    def session(self):
        return self.__session
