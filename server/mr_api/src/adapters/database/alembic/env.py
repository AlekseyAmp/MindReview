from alembic import context
from sqlalchemy import MetaData, engine_from_config, pool

from src.adapters.database import common_metadata, data_metadata, logs_metadata
from src.adapters.database.settings import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def combine_metadata(*args):
    m = MetaData()
    for metadata in args:
        for t in metadata.tables.values():
            t.tometadata(m)
    return m


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = combine_metadata(
    common_metadata,
    data_metadata,
    logs_metadata,
)


def run_migrations_offline():
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        include_schemas=True,
        version_table_schema=target_metadata.schema,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """

    def include_name(name, type_, parent_names):
        if type_ == "table":
            return (
                parent_names["schema_qualified_table_name"]
                in target_metadata.tables
            )
        else:
            return True

    configuration = config.get_section(config.config_ini_section)
    configuration['sqlalchemy.url'] = settings.SQLALCHEMY_DB_URL
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            version_table_schema=target_metadata.schema,
            include_name=include_name
        )

        with context.begin_transaction():
            # этот костыль только для БД MSSQL
            # связано с инфраструктурными особенностями
            # connection.execute(
            #     f"if schema_id('{target_metadata.schema}') is null "
            #     f"execute('create schema {target_metadata.schema}')"
            # )

            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
