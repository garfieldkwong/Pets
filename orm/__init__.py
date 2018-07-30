"""ORM"""
import sqlalchemy
from . import base, constants

def open_db_engine():
    """Open database engine"""
    db_engine = sqlalchemy.create_engine(
        constants.DB_URL
    )
    return db_engine
