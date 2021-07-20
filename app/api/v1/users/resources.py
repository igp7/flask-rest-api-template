import logging
from flask import Blueprint, request, jsonify, make_response
from flask.views import MethodView
from marshmallow import ValidationError
from app.api.v1.schemas import UsersSchema
from app.api.models import Users
from app.common.error_handling import NotFoundException, ValidationException, UnauthorizedException, \
    BadRequestException, ForbiddenException
from flask_jwt_extended import jwt_required
from app.common.utils import admin_required, is_current_user, current_user_is_admin, \
    is_not_admin_and_is_not_current_user

# Crear logger para este modulo
logger = logging.getLogger(__name__)

# Crear Blueprint de users
users_bp = Blueprint('users_bp', __name__)

# Crear instancia del esquema de users
users_schema = UsersSchema()
user_schema = UsersSchema(exclude=['tokens'])


class UsersAPI(MethodView):
    @jwt_required()
    @admin_required
    def get(self):
        logger.info(f"Peticion GET de todos Users.")
        users = Users.get_all()

        try:
            result = users_schema.dump(users, many=True)
        except ValidationError as err:
            logger.info(f"Error en dump schema.")
            raise ValidationException(err.messages)

        return make_response(jsonify({"status": 200,
                                      "msg": "Get de usuarios con exito.",
                                      "data": result}), 200)

    def post(self):
        logger.info(f"Peticion POST para crear un nuevo user.")

        try:
            data = request.get_json()
        except:
            logger.info(f"Falta body en la request.")
            raise BadRequestException(f"Falta body en la request.")

        if 'name' not in data or 'password' not in data:
            logger.info(f"Falta name o password.")
            raise BadRequestException(f"Falta name o password.")

        try:
            user_dict = users_schema.load(data)
        except ValidationError as err:
            logger.info("Error en validacion de load schema.")
            raise ValidationException(err.messages)

        user = Users(name=user_dict['name'], password=user_dict['password'], admin=False)
        user.save()
        logger.info(f"Nuevo usuario registrado.")
        try:
            result = users_schema.dump(user)
        except ValidationError as err:
            logger.info(f"Error en dump schema")
            raise ValidationException(err.messages)

        return make_response(jsonify({"status": 201,
                                      "msg": "Usuario creado con exito.",
                                      "data": result}), 201)


class UserAPI(MethodView):
    @jwt_required()
    def get(self, public_id):
        logger.info(f"Peticion GET User")
        logger.debug(f"Peticion GET del usuario {public_id}")
        user = Users.simple_filter(public_id=public_id)
        if not user:
            logger.debug(f"No existe el usuario {public_id}.")
            raise NotFoundException(f"El usuario no existe.")

        if not is_current_user(public_id) and not current_user_is_admin():
            logger.debug(f"No tiene acceso al usuario con public_id {public_id}.")
            raise UnauthorizedException(f"No tiene acceso al usuario con public_id {public_id}.")

        try:
            result = user_schema.dump(user)
        except ValidationError as err:
            logger.debug(f"Error en dump schema.")
            raise ValidationException(err.messages)

        return make_response(jsonify({"status": 200,
                                      "msg": "Get de usuario con exito.",
                                      "data": result}), 200)

    @jwt_required()
    def put(self, public_id):
        logger.info(f"Peticion PUT para actualizar usuario.")
        logger.debug(f"Peticion PUT para actualizar al usuario {public_id}.")

        try:
            data = request.get_json()
        except:
            logger.debug(f"Falta body en la request.")
            raise BadRequestException(f"Falta body en la request.")

        try:
            user_dict = users_schema.load(data, partial=True)
        except ValidationError as err:
            logger.debug(f"Error en load schema.")
            raise ValidationException(err.messages)

        user = Users.simple_filter(public_id=public_id)
        if not user:
            logger.debug(f"No existe el usuario {public_id}.")
            raise NotFoundException(f"No existe el usuario {public_id}.")

        user.update_user(**user_dict)
        user.save()
        logger.info(f"Usuario actualizado.")

        try:
            result = users_schema.dump(user)
        except ValidationError as err:
            logger.debug(f"Error en dump schema.")
            raise ValidationException(err.messages)

        return make_response(jsonify({"status": 201,
                                      "msg": "Usuario actualizado con exito.",
                                      "data": result}), 201)

    @jwt_required()
    def delete(self, public_id):
        logger.info(f"Peticion DELETE de usuario.")
        logger.debug(f"Peticion DELETE del usuario {public_id}.")

        if is_not_admin_and_is_not_current_user(public_id):
            logger.debug(f"Necesario ser admin o el usuario a eliminar.")
            raise ForbiddenException(f"Necesario ser admin o el usuario a eliminar.")

        user = Users.simple_filter(public_id=public_id)
        if not user:
            logger.debug(f"No existe el usuario {public_id}.")
            raise NotFoundException(f"No existe el usuario {public_id}.")

        try:
            result = users_schema.dump(user)
        except ValidationError as err:
            logger.debug(f"Error en dump user.")
            raise ValidationException(err.messages)

        user.delete()
        logger.info(f"Usuario eliminado.")
        logger.debug(f"Eliminado el usuario {public_id}.")

        return make_response(jsonify({"status": 200,
                                      "msg": "Usuario eliminado con exito.",
                                      "data": result}), 200)


users_view = UsersAPI.as_view('users_api')
users_bp.add_url_rule('/users',
                      view_func=users_view,
                      methods=['GET', 'POST'])

user_view = UserAPI.as_view('user_api')
users_bp.add_url_rule('/users/<string:public_id>',
                      view_func=user_view,
                      methods=['GET', 'PUT', 'DELETE'])
