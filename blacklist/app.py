import os
import logging
from typing import Optional
from flask import Flask
from flask_restful import Api

from blacklist.api.views.auth import initialize_routes as initialize_auth_routes
from blacklist.api.views.list import initialize_routes as initialize_list_routes
from blacklist.api.views.core import initialize_routes as initialize_core_routes
from blacklist.extensions import db, jwt

LOGGER = logging.getLogger()


def create_app(script_info=None)  -> Flask:
    # instantiate the app
    app = Flask(
        __name__,
    )
    api = Api(app)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)
    app.config.from_prefixed_env()
    configure_extensions(app)

    LOGGER.info('Starting app with %s settings', app_settings)

    initialize_auth_routes(api)
    initialize_list_routes(api)
    initialize_core_routes(api)

    # shell context for flask cli
    app.shell_context_processor({"app": app})

    return app


def configure_extensions(app: Flask) -> None:
    """Configure flask extensions"""
    db.init_app(app)
    import blacklist.models
    jwt.init_app(app)