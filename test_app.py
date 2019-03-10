import unittest
import app

class ContactsApiTest(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
