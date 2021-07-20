import json
from app.api.models import Users
from app.common.error_handling import UnauthorizedException


def get_tokens(client, app):
    with app.app_context():
        name_user = 'token_user'
        endpoint = '/auth/login'
        password_user_token = '1234'

        payload = {'name': name_user,
                   'password': password_user_token}

        # Peticion para optener un access token
        response = post_login(client, endpoint, data=payload)

        access_token = response.json['data']['access_token']
        refresh_token = response.json['data']['refresh_token']
        if not access_token or not refresh_token:
            raise UnauthorizedException("Error en generar token para tests")

        return {'access_token': access_token, 'refresh_token': refresh_token}


def post_login(client, endpoint, data=None):
    response = client.post(endpoint, headers={"Content-Type": "application/json"},
                           data=json.dumps(data))
    return response


def get_refresh(client, app, endpoint, data=None):
    tokens = get_tokens(client, app)
    authorization = f"Bearer {tokens['refresh_token']}"
    response = client.get(endpoint, headers={"Content-Type": "application/json",
                                             "Authorization": authorization}, data=data)
    return response


def get(client, app, endpoint, data=None):
    tokens = get_tokens(client, app)
    authorization = f"Bearer {tokens['access_token']}"
    response = client.get(endpoint, headers={"Content-Type": "application/json",
                                             "Authorization": authorization}, data=data)
    return response


def post(client, app, endpoint, data=None):
    tokens = get_tokens(client, app)
    authorization = f"Bearer {tokens['access_token']}"
    response = client.post(endpoint, headers={"Content-Type": "application/json",
                                              "Authorization": authorization}, data=data)
    return response


def put(client, app, endpoint, data=None):
    tokens = get_tokens(client, app)
    authorization = f"Bearer {tokens['access_token']}"
    response = client.put(endpoint, headers={"Content-Type": "application/json",
                                             "Authorization": authorization}, data=data)
    return response


def delete(client, app, endpoint, data=None):
    tokens = get_tokens(client, app)
    authorization = f"Bearer {tokens['access_token']}"
    response = client.delete(endpoint, headers={"Content-Type": "application/json",
                                                "Authorization": authorization}, data=data)
    return response


def create_user(app, name='user_test', password='12345', admin=False):
    with app.app_context():
        user = Users(name=name, password=password, admin=admin)
        user.save()
        return user.public_id


def create_user_token(app, name_token_user='token_user', password_token_user='1234', admin_token_user=False):
    create_user(app, name=name_token_user, password=password_token_user, admin=admin_token_user)
