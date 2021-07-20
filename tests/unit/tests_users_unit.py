import os
import unittest
from werkzeug.security import check_password_hash
from app.api.models import Users
from app import db, create_app


class UsersUnitTests(unittest.TestCase):

    # SETUP AND TEARDOWN
    # Se ejecutan antes de cada test
    def setUp(self):
        self.app = create_app(settings_module=os.environ.get('APP_TEST_SETTINGS_MODULE'))
        with self.app.app_context():
            # Crea las tablas de la base de datos
            db.create_all()

    # Se ejecutan despues de cada test
    def tearDown(self):
        with self.app.app_context():
            # Elimina todas las tablas de la base de datos
            db.session.remove()
            db.drop_all()

    # TESTS
    def test_create_user_success(self):
        # Give
        name = 'test_user'
        password = '1234'
        admin = False

        # When
        with self.app.app_context():
            user = Users(name=name, password=password, admin=admin)

        # Then
        self.assertEqual(str, type(user.public_id))
        self.assertEqual(name, user.name)
        self.assertTrue(check_password_hash(user.password, password))
        self.assertEqual(admin, user.admin)


if __name__ == '__main__':
    unittest.main()
