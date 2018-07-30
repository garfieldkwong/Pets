"""Pet model"""
from sqlalchemy import Column, Integer, String, DateTime
from . import base


class Pet(base.Base):
    """Pet model"""
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    available_from = Column(DateTime)
    age = Column(Integer)
    species = Column(String)
    breed = Column(String, nullable=True)

    @property
    def has_breed(self):
        return self.species == 'dog'


