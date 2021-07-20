import logging
from functools import wraps
from flask_jwt_extended import get_jwt_identity

from app.ext import jwt
from app.api.models import Users, BlacklistToken
from app.common.error_handling import ForbiddenException

# Crear logger para este modulo
logger = logging.getLogger(__name__)


def admin_required(f):
    """
    Decorador que comprueba si un usuario es admin.
    :param f:
    :return:
    """
    @wraps(f)
    def decorated_function(*args, **kws):
        if not current_user_is_admin():
            logger.info("Necesario ser admin")
            raise ForbiddenException("Necesario ser admin")
        return f(*args, **kws)
    return decorated_function


def is_not_admin_and_is_not_current_user(public_id):
    """
    Comprueba si un usuario es admin o es el usuario propietario del token.
    :param public_id:
    :return:
    """
    return not current_user_is_admin() and not is_current_user(public_id)


def current_user_is_admin():
    """
    Comprueba si el usuario actual es admin.
    :return:
    """
    user_public_id = get_jwt_identity()
    user = Users.simple_filter(public_id=user_public_id)
    return user.is_admin()


def is_current_user(public_id):
    """
    Comprueba si el usuario con public_id es el propietario del token.
    :param public_id:
    :return:
    """
    current_user_public_id = get_jwt_identity()
    return current_user_public_id == public_id


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    """
    Blacklist Token JWT.
    """
    jti = jwt_payload["jti"]
    return BlacklistToken.check_blacklist(jti)
