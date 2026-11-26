"""Alembic environment: wires migrations to our models and database URL."""

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from validationops.config import settings
from validationops.db.base import Base, sqlalchemy_url
from validationops.db.models import FailureEvent, WebhookDelivery  # noqa: F401

config = context.config

# Use the application's own database URL (from env / .env / defaults).
config.set_main_option("sqlalchemy.url", sqlalchemy_url(settings.database_url))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Alembic compares this metadata against the database when autogenerating.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Generate SQL without a live DB connection (alembic ... --sql)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations against a live database."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
