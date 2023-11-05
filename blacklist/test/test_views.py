import unittest
import uuid

from blacklist.app import create_app
from blacklist.extensions import db


class TestBlacklist(unittest.TestCase):
    def setUp(self):
        self.app = create_app({'TESTING': True})
        self.app_context = self.app.app_context()
        self.client = self.app.test_client()
        self.app_context.push()
        self.token = None

        with self.app.app_context():
            db.drop_all()
            db.create_all()

        self.client.post('/sign-up', json={
            "email": "pepe@correo.com",
            "password": "12345",
            "password2": "12345"
        })
        response = self.client.post('/login', json={
            "email": "pepe@correo.com",
            "password": "12345"
        })
        json = response.get_json()
        self.token = json['token']

    def tearDown(self):
        self.app_context.pop()

    def test_health(self):
        response = self.client.get('/health')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "OK"})

    def test_login_view(self):
        # Simular una solicitud POST a /login
        data = {
            "email": "pepe@correo.com",
            "password": "12345"
        }
        response = self.client.post('/login', json=data)

        self.assertEqual(response.status_code, 200)  # Código de respuesta esperado
        self.assertEqual(response.get_json()["message"], "Success")

    def test_empty_login_view(self):
        data = {}
        response = self.client.post('/login', json=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["message"], "No input data provided")

    def test_invalid_user_login_view(self):
        data = {
            "email": "invalidemail@email.com",
            "password": "11111"
        }
        response = self.client.post('/login', json=data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()["message"], "Email or password incorrect")

    def test_signup_view(self):
        # Simular una solicitud POST a /sign-up
        data = {
            "email": "user@example.com",
            "password": "password123",
            "password2": "password123"
        }
        response = self.client.post('/sign-up', json=data)

        self.assertEqual(response.status_code, 200)  # Código de respuesta esperado
        self.assertEqual(response.get_json()["status"], "OK")

    def test_empty_signup_view(self):
        data = {}
        response = self.client.post('/sign-up', json=data)

        self.assertEqual(response.status_code, 400)  # Código de respuesta esperado
        self.assertEqual(response.get_json()["message"], "No input data provided")

    def test_signup_wrong_password_view(self):
        data = {
            "email": "user1@example.com",
            "password": "password123",
            "password2": "passord12"
        }
        response = self.client.post('/sign-up', json=data)

        self.assertEqual(response.status_code, 422)

    def test_add_blacklist_entry(self):
        data = {
            "email": "new@example.com",
            "blocked_reason": "New reason"
        }
        response = self.client.post(
            '/blacklists',
            json=data,
            headers={'Authorization': f'Bearer {self.token}'}
        )

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["message"], "Email añadido a la lista negra con éxito")

    def test_add_empty_blacklist_entry(self):
        data = {}
        response = self.client.post(
            '/blacklists', json=data, headers={'Authorization': f'Bearer {self.token}'})

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["message"], "No input data provided")

    def test_add_invalid_email_blacklist_entry(self):
        data = {
            "email": "test",
            "blocked_reason": "New reason"
        }
        response = self.client.post(
            '/blacklists', json=data, headers={'Authorization': f'Bearer {self.token}'})

        self.assertEqual(response.status_code, 422)

    def test_get_blacklist_entry(self):
        self.client.post(
            '/blacklists',
            json={
                "email": "exist@correo.com",
                "blocked_reason": "New reason"
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        response = self.client.get(
            '/blacklists/exist@correo.com',
            headers={'Authorization': f'Bearer {self.token}'}
        )

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["blacklisted"])
        self.assertEqual(data["reason"], "New reason")

    def test_get_non_existing_blacklist_entry(self):
        response = self.client.get(
            '/blacklists/nonexistent@example.com', headers={'Authorization': f'Bearer {self.token}'})

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data["blacklisted"])
        self.assertIsNone(data["reason"])
