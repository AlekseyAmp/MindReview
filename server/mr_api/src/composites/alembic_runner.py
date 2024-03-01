import sys

from alembic.config import CommandLine, Config

from src.adapters.database.settings import settings


def make_config() -> Config:
    config = Config()
    config.set_main_option(
        'script_location', settings.ALEMBIC_SCRIPT_LOCATION
    )
    config.set_main_option(
        'version_locations', settings.ALEMBIC_VERSION_LOCATIONS
    )
    config.set_main_option('sqlalchemy.url', settings.SQLALCHEMY_DB_URL)
    config.set_main_option(
        'file_template', settings.ALEMBIC_MIGRATION_FILENAME_TEMPLATE
    )
    config.set_main_option('timezone', 'UTC')

    return config


def run_cmd(*args) -> None:
    cli = CommandLine()
    cli.run_cmd(make_config(), cli.parser.parse_args(args))


if __name__ == '__main__':
    run_cmd(*sys.argv[1:])
