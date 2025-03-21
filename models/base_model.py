#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""

        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            dtf = "%Y-%m-%dT%H:%M:%S.%f"
            for att in kwargs:
                if att == 'created_at':
                    val = datetime.strptime(
                        kwargs['created_at'], dtf)
                    kwargs['created_at'] = val
                elif att == 'updated_at':
                    val2 = datetime.strptime(
                        kwargs['updated_at'], dtf)
                    kwargs['updated_at'] = val2

                if att != "__class__":
                    setattr(self, att, kwargs[att])
            else:
                self.id = str(uuid.uuid4())
                self.created_at = datetime.now()

    def __str__(self):
        """Returns a string representation of the instance"""

        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""

        from models import storage

        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""

        dictionary = {}
        dictionary.update(self.__dict__)
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        dictionary.update({'__class__': type(self).__name__})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        """ delete the current instance from the storage"""

        from models import storage

        storage.delete(self)
