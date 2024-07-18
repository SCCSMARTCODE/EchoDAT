"""
This module contain the base class for all the other classes
"""
from sqlalchemy import DateTime, Column, BOOLEAN, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
import datetime
from uuid import uuid4


class BaseModel:
    """
    This is the base class that will add 4 features to
        every class that inherit it
        0. _id
        1. created_at
        2. updated_at
        3. status

    """
    __abstract__ = True

    _id = Column(String(50), primary_key=True, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    status = Column(BOOLEAN, default=True, nullable=False)

    def __init__(self, *args, **kwargs):
        self._id = str(uuid4())
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

        if kwargs:
            self.__dict__.update(kwargs)

    def get_id(self):
        return str(self._id)


"""
Defining the Model the makes our model declarative
"""
metadata = MetaData()
Base = declarative_base(metadata=metadata)
