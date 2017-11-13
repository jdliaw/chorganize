import unittest
import requests

class TestUser(unittest.TestCase):
    def test_1(self):
        self.assertTrue(True)

    def test_2(self):
        self.assertTrue(True)

    def test_get_user_failsWithInvalidInput(self):
        response2 = requests.get("http://localhost:8080/api/user")
        self.assertEquals(response2.status_code, 400)

if __name__ == '__main__':
    unittest.main()