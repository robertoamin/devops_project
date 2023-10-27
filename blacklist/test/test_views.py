import unittest
from blacklist.app import create_app


class TestBlacklist(unittest.TestCase):
    def setUp(self):
        self.app = create_app({'TESTING': True})
        self.app_context = self.app.app_context()
        self.client = self.app.test_client()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_health(self):
        response = self.client.get('/health')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "OK"})