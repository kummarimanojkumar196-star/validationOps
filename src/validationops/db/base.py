"""SQLAlchemy engine, session factory, and the declarative Base.

Every ORM model inherits from Base; Alembic reads Base.metadata to know
which tables should exist.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from validationops.config import settings


def sqlalchemy_url(url: str) -> str:
    """Add the psycopg (v3) driver name that SQLAlchemy needs.

    config.py stores 'postgresql://...'; SQLAlchemy wants
    'postgresql+psycopg://...' so it uses the installed psycopg 3 driver.
    """
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


engine = create_engine(sqlalchemy_url(settings.database_url), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base class for all ORM models."""
