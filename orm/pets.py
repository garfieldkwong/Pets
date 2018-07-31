"""Pet model"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, or_
from sqlalchemy.orm import relationship
from . import base, customers, utils


class Pet(base.Base):
    """Pet model"""
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    available_from = Column(DateTime)
    age = Column(Integer)
    species = Column(String)
    breed = Column(String, nullable=True)
    adopt_to = Column(Integer, ForeignKey(customers.Customer.id), nullable=True)
    matched_customers = relationship(
        'Customer', secondary='matches', backref='Pet'
    )

    @property
    def has_breed(self):
        return utils.check_has_breed(self.species)

    @classmethod
    def query_with_perference(
            cls, db_conn, age_min=None, age_max=None,
            species=None, breed=None
    ):
        """Query pets with preference"""
        query = db_conn.query(
            Pet
        ).filter(cls.adopt_to.is_(None))
        if age_min is not None:
            query = query.filter(cls.age >= age_min)
        if age_max is not None:
            query = query.filter(cls.age <= age_max)
        if species is not None:
            query = query.filter(
                or_(cls.species.is_(None), cls.species.in_(species))
            )
        if breed is not None:
            query = query.filter(
                or_(cls.breed.is_(None), cls.breed.in_(breed))
            )
        return query.all()

    @classmethod
    def query_with_id(cls, db_conn, id):
        """Query with id"""
        query = db_conn.query(
            Pet
        ).filter(cls.id == id)
        return query.one_or_none()
