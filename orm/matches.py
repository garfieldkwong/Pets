"""Matched model"""
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey
from . import base
from . import customers, pets


class Match(base.Base):
    """Match model"""
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey(customers.Customer.id))
    pet_id = Column(Integer, ForeignKey(pets.Pet.id))

    @classmethod
    def query_matched_pets(cls, db_conn, customer_id, pet_id=None):
        """Query matched pets"""
        query = db_conn.query(
            customers.Customer
        ).outerjoin(
            Match
        ).outerjoin(
            pets.Pet
        ).filter(
            customers.Customer.id == customer_id
        )
        if pet_id is not None:
            query = query.filter(
                pets.Pet.id == pet_id
            )
        return query.one_or_none()

    @classmethod
    def query_matched_customers(cls, db_conn, pet_id):
        """Query matched pets"""
        query = db_conn.query(
            pets.Pet
        ).outerjoin(
            Match
        ).join(
            customers.Customer
        ).filter(
            pets.Pet.id == pet_id
        ).filter(
            pets.Pet.available_from <= datetime.now()
        )
        return query.one_or_none()
