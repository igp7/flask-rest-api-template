import os

from flask import Flask
from app.db import db
from .api.v1.auth.resources import auth_bp
from .api.v1.users.resources import users_bp
from .common.error_handling import register_error_handlers
from .common.logging import configure_logging
from .ext import ma, migrate, jwt, cors
import manage


def create_app(settings_module):
    app = Flask(__name__)
    app.config.from_object(settings_module)

    # Inicializa las extensiones
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    manage.init_app(app)

    # Configuracion de logging
    configure_logging(app)

    # Deshabilitar el modo estricto de acabado en una URL con /
    app.url_map.strict_slashes = False

    # Registrar los blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)

    # Registrar manejadores de errorres personalizados
    register_error_handlers(app)

    return app


settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(settings_module)