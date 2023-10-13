import logging
from flask.cli import FlaskGroup
from blacklist.app import create_app
from blacklist.extensions import db

LOGGER = logging.getLogger()

current_app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("create_db")
def create_db():
    """Create database migrations and upgrade it"""
    db.create_all()


@cli.command("drop_db")
def drop_db():
    """Drop all database"""
    db.drop_all()


if __name__ == "__main__":
    cli()
