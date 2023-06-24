#!/usr/bin/python3
"""Defines the Place class."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, backref
import os


place_amenity = Table(
        'place_amenity', Base.metadata,
        Column('place_id', String(60), ForeignKey('places.id'),
            primary_key=True, nullable=False),
        Column('amenity_id', String(60), ForeignKey('amenities.id'),
            primary_key=True, nullable=False))

class Place(BaseModel, Base):
    """Represents a Place for a MySQL database.

    Inherits from SQLAlchemy Base and links to the MySQL table places.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store places.
        city_id (sqlalchemy String): The place's city id.
        user_id (sqlalchemy String): The place's user id.
        name (sqlalchemy String): The name.
        description (sqlalchemy String): The description.
        number_rooms (sqlalchemy Integer): The number of rooms.
        number_bathrooms (sqlalchemy Integer): The number of bathrooms.
        max_guest (sqlalchemy Integer): The maximum number of guests.
        price_by_night (sqlalchemy Integer): The price by night.
        latitude (sqlalchemy Float): The place's latitude.
        longitude (sqlalchemy Float): The place's longitude.
    """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if os.environ['HBNB_TYPE_STORAGE'] == 'db':
        reviews = relationship("Review", backref="place", cascade="all,delete")
        amenities = relationship(
                'Amenity', secondary='place_amenity', viewonly=False)
    else:
        @property
        def reviews(self):
            """Getter attribute reviews that returns the list of Review
                instances with place_id equals to the current Place.id
            """

            from models import storage
            from models.review import Review

            a_list = []
            for review in storage.all(Review).values():
                if review.place_id == self.id:
                    a_list.append(review)
            return a_list

        @property
        def amenities(self):
            """ returns the list of Amenity instances based on the
                attribute amenity_ids that contains all Amenity.id
                linked to the Place
            """

            from models import storage
            from models.amenity import Amenity

            m_list = []
            for amenity in storage.all(Amenity).values:
                if amenity.id in self.amenity_ids:
                    m_list.append(amenity)
            return m_list

        @amenities.setter
        def amenities(self, obj):
            """ handles append method for adding an Amenity.id to the attribute
                amenity_ids. This method should accept only Amenity object,
                otherwise, do nothing
            """

            from models import storage
            from models.amenity import Amenity

            if type(obj) is Amenity:
                self.amenity_ids.append(obj.id)
            else:
                return
