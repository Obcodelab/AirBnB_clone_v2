#!/usr/bin/python3
""" Defining a DataBase storage """
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os


classes = {'Amenity': Amenity, 'City': City, 'Place': Place, 'State': State,
           'User': User, 'Review': Review}


class DBStorage:
    """A class defines DataBase storage using SQLAlchemy
    """
    __engine = None
    __session = None

    def __init__(self):
        """ Class constructor """

        username = os.environ.get('HBNB_MYSQL_USER')
        password = os.environ.get('HBNB_MYSQL_PWD')
        host = os.environ.get('HBNB_MYSQL_HOST')
        database = os.environ.get('HBNB_MYSQL_DB')

        create = (f'mysql+mysqldb://{username}:{password}@{host}/{database}')
        self.__engine = create_engine(create, pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query on the current database session (self.__session)
            all objects depending of the class name
        """
        a_dict = {}

        if cls is None:
            for cls in classes:
                for obj in self.__session.query(cls).all():
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    a_dict[key] = obj
        else:
            for obj in self.__session.query(cls).all():
                key = "{}.{}".format(type(obj).__name__, obj.id)
                a_dict[key] = obj
        return a_dict

    def new(self, obj):
        """ Add the object to the current database session """

        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """

        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session obj if not None"""
        if obj:
            c_name = type(obj).__name__
            obd = self.__session.query(c_name).filter(
                    obj.id.in_(c_name.id)).first()
            if obd:
                self.__session.delete(obd)

    def reload(self):
        """Create all tables and session for the database """

        Base.metadata.create_all(self.__engine)

        self.__session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))

    def close(self):
        """Remove private session attribute"""
        self.__session.close()
