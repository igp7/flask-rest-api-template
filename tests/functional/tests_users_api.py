import os
import unittest
import json
from app import db, create_app
from tests.common.helper_methods import get, post, put, delete, create_user


class UsersTestsApi(unittest.TestCase):

    # SETUP AND TEARDOWN
    # Se ejecutan antes de cada test
    def setUp(self):
        self.app = create_app(settings_module=os.environ.get('APP_TEST_SETTINGS_MODULE'))
        self.client = self.app.test_client()
        self.name = 'token_user'
        self.password = '1234'
        self.admin = True
        self.endpoint = '/users'
        self.public_id = None

        # Crea un contexto de aplicación
        with self.app.app_context():
            # Crea las tablas de la base de datos
            db.create_all()
            # Crear un user para los tests
            self.public_id = create_user(self.app, name=self.name, password=self.password, admin=self.admin)

    # Se ejecutan despues de cada test
    def tearDown(self):
        with self.app.app_context():
            # Elimina todas las tablas de la base de datos
            db.session.remove()
            db.drop_all()

    # TESTS
    def test_get_users_success(self):
        # Given
        client = self.client
        app = self.app
        endpoint = self.endpoint

        # When
        response = get(client=client, app=app, endpoint=endpoint)

        # Then
        self.assertLogs("Get de usuarios con exito.", response.json['msg'])
        self.assertEqual(200, response.json['status'])
        self.assertEqual(200, response.status_code)

    def test_get_user_success(self):
        # Given
        client = self.client
        app = self.app
        public_id = self.public_id
        name = self.name
        admin = self.admin
        endpoint = self.endpoint + '/{}'.format(public_id)

        # When
        response = get(client=client, app=app, endpoint=endpoint)

        # Then
        self.assertLogs("Get de usuario con exito.", response.json['msg'])
        self.assertEqual(public_id, response.json['data']['public_id'])
        self.assertEqual(name, response.json['data']['name'])
        self.assertEqual(admin, response.json['data']['admin'])
        self.assertEqual(200, response.json['status'])
        self.assertEqual(200, response.status_code)

    def test_get_user_invalid_user(self):
        # Given
        client = self.client
        app = self.app
        public_id = 'invalid_public_id'
        endpoint = self.endpoint + '/{}'.format(public_id)

        # When
        response = get(client=client, app=app, endpoint=endpoint)

        # Then
        self.assertLogs("El usuario no existe.", response.json['msg'])
        self.assertEqual(404, response.json['status'])
        self.assertEqual(404, response.status_code)

    def test_post_users_success(self):
        # Given
        client = self.client
        app = self.app
        admin = False
        name = "user_post_test"
        password = "123"
        endpoint = self.endpoint
        payload = json.dumps({
            "name": name,
            "password": password
        })

        # When
        response = post(client=client, app=app, endpoint=endpoint, data=payload)

        # Then
        self.assertLogs("Usuario creado con exito.", response.json['msg'])
        self.assertTrue(response.json['data']['public_id'])
        self.assertTrue(response.json['data']['userId'])
        self.assertTrue(response.json['data']['password'])
        self.assertEqual(name, response.json['data']['name'])
        self.assertEqual(admin, response.json['data']['admin'])
        self.assertEqual(201, response.json['status'])
        self.assertEqual(201, response.status_code)

    def test_post_users_no_unique_name(self):
        # Given
        client = self.client
        app = self.app
        name = "token_user"
        password = "123"
        endpoint = self.endpoint
        payload = json.dumps({
            "name": name,
            "password": password
        })

        # When
        response = post(client=client, app=app, endpoint=endpoint, data=payload)

        # Then
        self.assertEqual(f"El name {name} no esta disponible.", response.json['msg'])
        self.assertEqual(409, response.json['status'])
        self.assertEqual(409, response.status_code)

    def test_post_users_invalid_format_payload(self):
        # Given
        client = self.client
        app = self.app
        name = "user_post_test"
        password = 123
        endpoint = self.endpoint
        payload = json.dumps({
            "name": name,
            "password": password
        })

        # When
        response = post(client=client, app=app, endpoint=endpoint, data=payload)

        # Then
        self.assertLogs("Error en validacion de load schema", response.json['msg'])
        self.assertEqual(400, response.json['status'])
        self.assertEqual(400, response.status_code)

    def test_post_users_missing_payload(self):
        # Given
        client = self.client
        app = self.app
        endpoint = self.endpoint
        payload = None

        # When
        response = post(client=client, app=app, endpoint=endpoint, data=payload)

        # Then
        self.assertLogs("Falta body en la request", response.json['msg'])
        self.assertEqual(400, response.json['status'])
        self.assertEqual(400, response.status_code)

    def test_post_users_missing_name(self):
        # Given
        client = self.client
        app = self.app
        password = '123'
        endpoint = self.endpoint
        payload = json.dumps({
            "password": password
        })

        # When
        response = post(client=client, app=app, endpoint=endpoint, data=payload)

        # Then
        self.assertLogs("Falta name o password", response.json['msg'])
        self.assertEqual(400, response.json['status'])
        self.assertEqual(400, response.status_code)

    def test_post_users_missing_password(self):
        # Given
        client = self.client
        app = self.app
        name = "user_post_test"
        endpoint = self.endpoint
        payload = json.dumps({
            "name": name
        })

        # When
        response = post(client=client, app=app, endpoint=endpoint, data=payload)

        # Then
        self.assertLogs("Falta name o password", response.json['msg'])
        self.assertEqual(400, response.json['status'])
        self.assertEqual(400, response.status_code)

    def test_put_user_success(self):
        # Given
        client = self.client
        app = self.app
        public_id = self.public_id
        name = "test_put_user"
        password = "1234"
        admin = self.admin
        endpoint = self.endpoint + '/{}'.format(public_id)
        payload = json.dumps({
            "name": name,
            "password": password
        })

        # When
        response = put(client=client, app=app, endpoint=endpoint, data=payload)

        # Then
        self.assertLogs("Usuario actualizado con exito.", response.json['msg'])
        self.assertEqual(public_id, response.json['data']['public_id'])
        self.assertEqual(name, response.json['data']['name'])
        self.assertEqual(admin, response.json['data']['admin'])
        self.assertEqual(201, response.json['status'])
        self.assertEqual(201, response.status_code)

    def test_put_user_update_name_success(self):
        # Given
        client = self.client
        app = self.app
        public_id = self.public_id
        name = "test_put_user"
        admin = self.admin
        endpoint = self.endpoint + '/{}'.format(public_id)
        payload = json.dumps({
            "name": name
        })

        # When
        response = put(client=client, app=app, endpoint=endpoint, data=payload)

        # Then
        self.assertLogs("Usuario actualizado con exito.", response.json['msg'])
        self.assertEqual(public_id, response.json['data']['public_id'])
        self.assertEqual(name, response.json['data']['name'])
        self.assertEqual(admin, response.json['data']['admin'])
        self.assertEqual(201, response.json['status'])
        self.assertEqual(201, response.status_code)

    def test_put_user_update_password_success(self):
        # Given
        client = self.client
        app = self.app
        public_id = self.public_id
        password = "1234"
        admin = self.admin
        endpoint = self.endpoint + '/{}'.format(public_id)
        payload = json.dumps({
            "password": password
        })

        # When
        response = put(client=client, app=app, endpoint=endpoint, data=payload)

        # Then
        self.assertLogs("Usuario actualizado con exito.", response.json['msg'])
        self.assertEqual(public_id, response.json['data']['public_id'])
        self.assertEqual(admin, response.json['data']['admin'])
        self.assertEqual(201, response.json['status'])
        self.assertEqual(201, response.status_code)

    def test_put_user_missing_payload(self):
        # Given
        client = self.client
        app = self.app
        public_id = self.public_id
        endpoint = self.endpoint + '/{}'.format(public_id)
        payload = None

        # When
        response = put(client=client, app=app, endpoint=endpoint, data=payload)

        # Then
        self.assertLogs("Falta body en la request", response.json['msg'])
        self.assertEqual(400, response.json['status'])
        self.assertEqual(400, response.status_code)

    def test_put_user_invalid_format(self):
        # Given
        client = self.client
        app = self.app
        public_id = self.public_id
        name = "test_put_user"
        password = 1234
        endpoint = self.endpoint + '/{}'.format(public_id)
        payload = json.dumps({
            "name": name,
            "password": password
        })

        # When
        response = put(client=client, app=app, endpoint=endpoint, data=payload)

        # Then
        self.assertLogs("Error en load schema", response.json['msg'])
        self.assertEqual(400, response.json['status'])
        self.assertEqual(400, response.status_code)

    def test_put_user_invalid_public_id(self):
        # Given
        client = self.client
        app = self.app
        public_id = 'invalid_public_id'
        name = "test_put_user"
        password = '1234'
        endpoint = self.endpoint + '/{}'.format(public_id)
        payload = json.dumps({
            "name": name,
            "password": password
        })

        # When
        response = put(client=client, app=app, endpoint=endpoint, data=payload)

        # Then
        self.assertLogs("No existe el usuario {}".format(public_id), response.json['msg'])
        self.assertEqual(404, response.json['status'])
        self.assertEqual(404, response.status_code)

    def test_delete_user_success(self):
        # Given
        client = self.client
        app = self.app
        name = self.name
        public_id = self.public_id
        admin = self.admin
        endpoint = self.endpoint + '/{}'.format(public_id)

        # When
        response = delete(client=client, app=app, endpoint=endpoint)

        # Then
        self.assertLogs("Usuario eliminado con exito.", response.json['msg'])
        self.assertEqual(public_id, response.json['data']['public_id'])
        self.assertEqual(name, response.json['data']['name'])
        self.assertEqual(admin, response.json['data']['admin'])
        self.assertEqual(200, response.json['status'])
        self.assertEqual(200, response.status_code)

    def test_delete_user_invalid_public_id(self):
        # Given
        client = self.client
        app = self.app
        public_id = 'invalid_public_id'
        endpoint = self.endpoint + '/{}'.format(public_id)

        # When
        response = delete(client=client, app=app, endpoint=endpoint)

        # Then
        self.assertLogs("No existe el usuario {}".format(public_id), response.json['msg'])
        self.assertEqual(404, response.json['status'])
        self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    unittest.main()
