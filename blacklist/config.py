import os

basedir = os.path.abspath(os.path.dirname(__file__))



class BaseConfig(object):
    """Base configuration."""
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    CELERY = "config.DevelopmentCeleryConfig"



class ProductionConfig(BaseConfig):
    """Production configuration."""


