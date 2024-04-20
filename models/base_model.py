#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
from datetime import datetime
import models
from os import getenv
import sqlalchemy
from sqlalchemy import String, Column, Datetime
from sqlalchemy.ext.declarative import declarative_base
import uuid

time = "%Y-%m-%dT%H:%M:%S.%f"

if models.storage_t == "db":
	Base = declarative_base()
else:
	Base = object

class BaseModel:
    """A base class for all hbnb models"""

    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(Datetime, default=datetime.now)
        updated_at = Column(Datetime, default=datetime.now)

    
    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""

        if kwargs:
            for key, value in kwargs.items:
                if key != __class__:
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.updated_at) is str:
                 self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                 self.updated_at = datetime.now()
            if kwargs.get("id", None) is None:
                 self.id = str(uuid.uuid4())
        else:
             self.id = str(uuid.uuid4())
             self.created_at = datetime.now()
             self.updated_at = self.created_at

    def __str__(self) -> str:
         """Return a string representation of the instance"""
         return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save

    def to_dict(self):
        """Convert instance into dict format"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
             new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
             new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
             del new_dict["_sa_instance_state"]
        return new_dict
    
    def delete(self):
         """delete the current instance from storage"""
         models.storage.delete(self)