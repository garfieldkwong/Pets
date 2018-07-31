"""Customers model"""
from sqlalchemy import Column, Integer, ForeignKey, String, or_
from sqlalchemy.orm import relationship
from . import base, utils


class Customer(base.Base):
    """Pet model"""
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    preference_age = relationship('PreferenceAge')
    preference_species = relationship('PreferenceSpecies')
    preference_breed = relationship('PreferenceBreed')
    matched_pets = relationship('Pet', secondary='matches', backref='Customer')
    adopted_pets = relationship('Pet')

    @classmethod
    def query_with_id(cls, db_conn, id=None):
        """Query customer by id"""
        query = db_conn.query(
            Customer
        ).join(
            PreferenceAge
        ).outerjoin(
            PreferenceSpecies
        ).outerjoin(
            PreferenceBreed
        )
        if id is not None:
            query = query.filter(cls.id == id)
        return query.all()

    @classmethod
    def query_only_customer_with_id(cls, db_conn, id):
        """Query with id"""
        query = db_conn.query(
            Customer
        ).filter(cls.id == id)
        return query.one_or_none()

    @classmethod
    def query_with_preference(cls, db_conn, age, species, breed=None):
        """Query with preference"""
        query = db_conn.query(
            Customer
        ).join(
            PreferenceAge
        ).outerjoin(
            PreferenceSpecies
        ).outerjoin(
            PreferenceBreed
        ).filter(
            or_(PreferenceAge.min <= age, age <= PreferenceAge.max)
        ).filter(
            or_(PreferenceSpecies.name == species, PreferenceSpecies.name.is_(None))
        )
        if utils.check_has_breed(species) and breed is not None:
            query = query.filter(
                or_(PreferenceBreed.name == breed, preferenceBreed.name.is_(None))
            )
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
