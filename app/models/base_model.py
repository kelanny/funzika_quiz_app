#!/usr/bin/python3
"""
Contains the BaseModel class
"""

from datetime import datetime
from app import db
import uuid

time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel(db.Model):
    """This class defines all common attributes and methods for other
    classes.

    Attributes:
        id (uuid.uuid4): Unique identification number of class instances.
        created_at (datetime): Datetime when an instance is created.
        updated_at (datetime): Datetime when an instance was updated.

    Methods:
        __str__(): Returns a string representation of a class instance
        save: Updates the 'updated_at' attribute with the current datetime
        to_dict: Returns a dictionary containing all keys/values of the
                __dict__ of the instance
     """
    __abstract__ = True

    id = db.Column(db.String(60), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self):
        """Instantiates a new model or recreates an existing model"""
        super().__init__()
        # Create a new model
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def __str__(self):
        """Returns a string representation of the instance"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """Updates the 'updated_at' attribute with the current datetime"""
        self.updated_at = datetime.now()
        db.session.commit()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of the __dict__
        of the instance"""
        dictionary = dict(self.__dict__)
        return dictionary