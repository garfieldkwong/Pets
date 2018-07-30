"""Base class for model"""
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def create_all_tables(engine):
    Base.metadata.create_all(engine)