import orm
import routes
from orm import base
from sqlalchemy.orm import scoped_session, sessionmaker
from tornado import ioloop, web


db_engine = orm.open_db_engine()
db_session = sessionmaker()


class Application(web.Application):
    """Custom application"""
    def __init__(self, *args, **kwargs):
        """init"""
        super().__init__(*args, **kwargs)
        self.db = scoped_session(
            sessionmaker(
                bind=db_engine,
                autocommit=False, autoflush=True,
                expire_on_commit=False
            )
        )

    def create_database(self):
        """Create database"""
        base.create_all_tables(db_engine)

def make_app():
    app = Application(routes.URLs, db_session=db_session)
    app.create_database()
    return app


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    ioloop.IOLoop.current().start()
