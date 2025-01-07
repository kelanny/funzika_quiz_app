#!/usr/bin/python3
"""
Contains the BaseModel class.
"""
from datetime import datetime
from app import db
import uuid


class BaseModel(db.Model):
    """
    This class defines all common attributes and methods for other models.

    Attributes:
        id (str): Unique identification number of class instances.
        created_at (datetime): Datetime when an instance is created.
        updated_at (datetime): Datetime when an instance was last updated.

    Methods:
        __str__(): Returns a string representation of a class instance.
        save_to_db(): Saves the instance to the database.
        delete_from_db(): Deletes the instance from the database.
        to_dict(): Returns a dictionary representation of the instance.
    """
    __abstract__ = True

    id = db.Column(db.String(60), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime,
                           default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    def __str__(self):
        """Returns a string representation of the instance."""
        return f"<{self.__class__.__name__} {self.id}>"

    def save_to_db(self):
        """Saves the instance to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Deletes the instance from the database."""
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of the instance.

        Omits SQLAlchemy internal state.
        """
        dictionary = {key: value for key, value in self.__dict__.items()
                      if not key.startswith("_")}
        dictionary["created_at"] = self.created_at.isoformat() \
            if self.created_at else None
        dictionary["updated_at"] = self.updated_at.isoformat() \
            if self.updated_at else None
        return dictionary
