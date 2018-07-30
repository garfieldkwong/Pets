"""Customers model"""
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from . import base


class Customer(base.Base):
    """Pet model"""
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    preference_age = relationship('PreferenceAge')
    preference_species = relationship('PreferenceSpecies')
    preference_breed = relationship('PreferenceBreed')

    @classmethod
    def query_customers_by_id(cls, db_conn, id=None):
        """Query customer by id"""
        query = db_conn.query(
            Customer
        ).join(
            PreferenceAge
        ).join(
            PreferenceSpecies
        ).join(
            PreferenceBreed
        )
        if id is not None:
            query = query.filter(Customer.id == id)
        return query.all()


class PreferenceAge(base.Base):
    """Pet model"""
    __tablename__ = 'preference_age'
    id = Column(Integer, primary_key=True, autoincrement=True)
    min = Column(Integer, nullable=True)
    max = Column(Integer, nullable=True)
    customer_id = Column(Integer, ForeignKey(Customer.id))


class PreferenceSpecies(base.Base):
    """Pet model"""
    __tablename__ = 'preference_species'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    customer_id = Column(Integer, ForeignKey(Customer.id))



class PreferenceBreed(base.Base):
    """Pet model"""
    __tablename__ = 'preference_breed'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    customer_id = Column(Integer, ForeignKey(Customer.id))


