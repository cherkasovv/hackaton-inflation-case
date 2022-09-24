
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from core.config import settings
from contextvars import ContextVar

scope = ContextVar("scope_db_session")


def scopefunc():
    return scope.get()


engine = create_engine(settings.database_url)
current_session = scoped_session(sessionmaker(engine), scopefunc=scopefunc)
