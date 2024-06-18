"""
This module contain the base class for all the other classes
"""
from sqlalchemy import DATETIME, Column, BOOLEAN, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
import datetime
from uuid import uuid4


class BaseModel(object):
    """
    This is the base class that will add 4 features to
        every class that inherit it
        0. _id
        1. created_at
        2. updated_at
        3. status

    """

    __abstract__ = True

    _id = Column(String(50), primary_key=True, default=uuid4(), unique=True, nullable=False)
    created_at = Column(DATETIME, default=datetime.datetime.utcnow(), nullable=False)
    updated_at = Column(DATETIME, default=datetime.datetime.utcnow(), nullable=False)
    status = Column(BOOLEAN, default=True, nullable=False)


"""
Defining the Model the makes our model declarative
"""
metadata = MetaData()
Base = declarative_base(metadata=metadata)
