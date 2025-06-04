import os
import importlib
from dotenv import load_dotenv
from logging.config import fileConfig

import alembic_postgresql_enum
from sqlalchemy import engine_from_config
from sqlalchemy import create_engine
from sqlalchemy import pool
from sqlalchemy.dialects import postgresql

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

load_dotenv()
models_folder = os.getenv("MODELS_FOLDER")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")

model_folder_prefix = models_folder.replace("/", ".").rstrip(".")
db_url = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'

def _load_models() -> None:
    for filename in os.listdir(models_folder):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            full_import_path = f"{model_folder_prefix}.{module_name}"
            importlib.import_module(full_import_path)

def _get_base_model_metadata():
    base_module_path = f'{model_folder_prefix}.base'
    metadata_module = importlib.import_module(base_module_path)
    return metadata_module.Base.metadata

_load_models()
target_metadata = _get_base_model_metadata()

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # connectable = engine_from_config(
    #     config.get_section(config.config_ini_section, {}),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )

    # THE DEFAULT engine_from_config IS REPLACED BY FOLOWING LINE FOR DYNAMIC 
    # LOADING DATA FRON .env FILE
    connectable = create_engine(db_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
