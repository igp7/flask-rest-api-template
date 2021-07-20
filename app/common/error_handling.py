from flask import jsonify, make_response


class AppErrorBaseClass(Exception):
    """
    Base Exception
    """
    pass


class BadRequestException(AppErrorBaseClass):
    """
    400 Bad Request Exception
    """
    pass


class ValidationException(AppErrorBaseClass):
    """
    400 Validation Exception
    """
    pass


class UnauthorizedException(AppErrorBaseClass):
    """
    401 UNAUTHORIZED EXCEPTION
    """
    pass


class ForbiddenException(AppErrorBaseClass):
    """
    403 FORBIDDEN EXCEPTION
    """
    pass


class NotFoundException(AppErrorBaseClass):
    """
    404 NOT FOUND EXCEPTION
    """
    pass


class ConflictException(AppErrorBaseClass):
    """
    409 CONFLICT
    """
    pass


def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception_error(e):
        return make_response(jsonify({'status': 500, 'msg': 'Internal server error'}), 500)

    @app.errorhandler(401)
    def handle_401_error(e):
        return make_response(jsonify({'status': 401, 'msg': 'Unauthorized error'}), 401)

    @app.errorhandler(403)
    def handle_403_error(e):
        return make_response(jsonify({'status': 403, 'msg': 'Forbidden error'}), 403)

    @app.errorhandler(404)
    def handle_404_error(e):
        return make_response(jsonify({'status': 404, 'msg': 'Not Found error'}), 404)

    @app.errorhandler(405)
    def handle_405_error(e):
        return make_response(jsonify({'status': 405, 'msg': 'Method not allowed'}), 405)

    @app.errorhandler(BadRequestException)
    def handle_bad_request_error(e):
        return make_response(jsonify({'status': 400, 'msg': str(e)}), 400)

    @app.errorhandler(ValidationException)
    def handle_validation_error(e):
        return make_response(jsonify({'status': 400, 'msg': str(e)}), 400)

    @app.errorhandler(UnauthorizedException)
    def handle_unauthorized_error(e):
        return make_response(jsonify({'status': 401, 'msg': str(e)}), 401)

    @app.errorhandler(ForbiddenException)
    def handle_forbidden_error(e):
        return make_response(jsonify({'status': 403, 'msg': str(e)}), 403)

    @app.errorhandler(NotFoundException)
    def handle_not_found_error(e):
        return make_response(jsonify({'status': 404, 'msg': str(e)}), 404)

    @app.errorhandler(ConflictException)
    def handle_conflict_error(e):
        return make_response(jsonify({'status': 409, 'msg': str(e)}), 409)
