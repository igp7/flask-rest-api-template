import logging
from flask import Blueprint, request, jsonify, make_response
from flask.views import MethodView
from app.api.models import Users, BlacklistToken
from app.common.error_handling import BadRequestException, NotFoundException
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from werkzeug.security import check_password_hash

# Crear logger para este modulo
logger = logging.getLogger(__name__)

# Crear Blueprint de auth
auth_bp = Blueprint('auth_bp', __name__)


class LoginAPI(MethodView):
    def post(self):
        logger.info(f"Peticion POST para logearse")

        auth = request.get_json()
        if not auth or 'name' not in auth or 'password' not in auth:
            logger.info(f"Falta name o password")
            raise BadRequestException(f"Falta name o password")

        logger.info(f"Peticion de login del usuario {auth['name']}.")
        user = Users.simple_filter(name=auth['name'])
        if not user:
            logger.info(f"No existe el user (usar el name en name).")
            raise NotFoundException(f"No existe el user (usar el name en name).")

        if not check_password_hash(user.password, auth['password']):
            logger.info(f"Contraseña no valida")
            raise BadRequestException(f"Contraseña no valida")

        access_token = user.create_access_token()
        refresh_token = user.create_refresh_token()

        logger.info(f"El usuario {user.name} a creado el access token {access_token}")
        logger.info(f"El usuario {user.name} a creado el refresh token {refresh_token}")

        result = {
            'public_id': user.public_id,
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return make_response(jsonify({"status": 200,
                                      "msg": "Login con exito.",
                                      "data": result}), 200)


class LogoutAPI(MethodView):
    @jwt_required()
    def delete(self):
        jti = get_jwt()['jti']
        token_type = get_jwt()['type']
        user_identity = get_jwt_identity()
        exp = get_jwt()['exp']

        blacklist_token = BlacklistToken(
            jti=jti,
            token_type=token_type,
            user_identity=user_identity,
            exp=exp)

        blacklist_token.save()

        return make_response(jsonify({"status": 200,
                                      "msg": "Logout con exito."}), 200)


class RefreshAPI(MethodView):
    @jwt_required(refresh=True)
    def get(self):
        current_user = get_jwt_identity()

        user = Users.simple_filter(public_id=current_user)
        if not user:
            logger.info(f"No existe el usuario con public_id {current_user}.")
            raise NotFoundException(f"No existe el usuario con public_id {current_user}.")

        result = {
            'access_token': user.create_access_token()
        }

        return make_response(jsonify({"status": 200,
                                      "msg": "Refresh con exito.",
                                      "data": result}), 200)


login_view = LoginAPI.as_view('login_api')
auth_bp.add_url_rule('/auth/login', view_func=login_view, methods=['POST'])

logout_view = LogoutAPI.as_view('logout_api')
auth_bp.add_url_rule('/auth/logout', view_func=logout_view, methods=['DELETE'])

refresh_view = RefreshAPI.as_view('refresh_api')
auth_bp.add_url_rule('/auth/refresh', view_func=refresh_view, methods=['GET'])
