import os
import unittest
from app import db, create_app
from tests.common.helper_methods import delete, create_user, post_login, get_refresh


class AuthTestsApi(unittest.TestCase):

    # SETUP AND TEARDOWN
    # Se ejecutan antes de cada test
    def setUp(self):
        self.app = create_app(settings_module=os.environ.get('APP_TEST_SETTINGS_MODULE'))
        self.client = self.app.test_client()
        self.name = 'token_user'
        self.password = '1234'
        self.admin = True
        self.endpoint = '/auth'
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
    def test_login_success(self):
        # Given
        client = self.client
        endpoint = f"{self.endpoint}/login"
        public_id = self.public_id
        name = self.name
        password = self.password
        payload = {'name': name,
                   'password': password}

        # When
        response = post_login(client, endpoint, data=payload)

        # Then
        self.assertEqual("Login con exito.", response.json['msg'])
        self.assertTrue(response.json['data'])
        self.assertTrue(response.json['data']['public_id'])
        self.assertEqual(public_id, response.json['data']['public_id'])
        self.assertTrue(response.json['data']['access_token'])
        self.assertTrue(response.json['data']['refresh_token'])
        self.assertEqual(200, response.json['status'])
        self.assertEqual(200, response.status_code)

    def test_login_missing_name(self):
        # Given
        client = self.client
        endpoint = f"{self.endpoint}/login"
        password = self.password
        payload = {'password': password}

        # When
        response = post_login(client, endpoint, data=payload)

        # Then
        self.assertEqual("Falta name o password", response.json['msg'])
        self.assertEqual(400, response.json['status'])
        self.assertEqual(400, response.status_code)

    def test_login_missing_password(self):
        # Given
        client = self.client
        endpoint = f"{self.endpoint}/login"
        name = self.name
        payload = {'name': name}

        # When
        response = post_login(client, endpoint, data=payload)

        # Then
        self.assertEqual("Falta name o password", response.json['msg'])
        self.assertEqual(400, response.json['status'])
        self.assertEqual(400, response.status_code)

    def test_login_missing_payload(self):
        # Given
        client = self.client
        endpoint = f"{self.endpoint}/login"
        payload = None

        # When
        response = post_login(client, endpoint, data=payload)

        # Then
        self.assertEqual("Falta name o password", response.json['msg'])
        self.assertEqual(400, response.json['status'])
        self.assertEqual(400, response.status_code)

    def test_login_invalid_name(self):
        # Given
        client = self.client
        endpoint = f"{self.endpoint}/login"
        password = self.password
        payload = {'name': '373y6rb',
                   'password': password}

        # When
        response = post_login(client, endpoint, data=payload)

        # Then
        self.assertEqual("No existe el user (usar el name en name).", response.json['msg'])
        self.assertEqual(404, response.json['status'])
        self.assertEqual(404, response.status_code)

    def test_login_invalid_password(self):
        # Given
        client = self.client
        endpoint = f"{self.endpoint}/login"
        name = self.name
        payload = {'name': name,
                   'password': 'error_password'}

        # When
        response = post_login(client, endpoint, data=payload)

        # Then
        self.assertEqual("Contraseña no valida", response.json['msg'])
        self.assertEqual(400, response.json['status'])
        self.assertEqual(400, response.status_code)

    def test_logout_success(self):
        # Given
        client = self.client
        app = self.app
        endpoint = f"{self.endpoint}/logout"
        payload = None

        # When
        response = delete(client, app, endpoint, data=payload)

        # Then
        self.assertEqual("Logout con exito.", response.json['msg'])
        self.assertEqual(200, response.json['status'])
        self.assertEqual(200, response.status_code)

    def test_refresh_success(self):
        # Given
        client = self.client
        app = self.app
        endpoint = f"{self.endpoint}/refresh"
        payload = None

        # When
        response = get_refresh(client, app, endpoint, data=payload)

        # Then
        self.assertEqual("Refresh con exito.", response.json['msg'])
        self.assertTrue(response.json['data'])
        self.assertTrue(response.json['data']['access_token'])
        self.assertEqual(200, response.json['status'])
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
