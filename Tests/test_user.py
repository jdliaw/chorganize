import unittest
import requests
import sys
sys.path.append('..')
from database_setup import createApp, db, User, Group


class TestUser(unittest.TestCase):
    ClassIsSetup = False

    def setUp(self):
        if not self.ClassIsSetup:
            self.setupClass()
            self.__class__.ClassIsSetup = True

    def setupClass(self):
        app = createApp(True)
        app.app_context().push()
        db.create_all()
        self.user1 = User.createUser("michael@ucla.edu", "Michael", "hello", "Michael", "Shea")
        self.user2 = User.createUser("kchan52@ucla.edu", "kaitlyne", "hello", "Kaitlyne", "Chan")
        self.user3 = User.createUser("hello@ucla.edu", "hello", "hello", "helloe", "hello")
        self.group = Group.createGroup("My Apartment")

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_delete_user(self):
        response2 = requests.post('http://localhost:8080/api/user/delete', data='{"email": "hello@ucla.edu}')
        self.assertEqual(response2.status_code, "User Successfully Removed")

    def test_get_user_fails_with_user_not_found(self):
        response2 = requests.get("http://localhost:8080/api/users?email=michael123@gmail.com")
        self.assertEqual(response2.status_code, 404)


    def test_get_user_fails_with_missing_input(self):
        response2 = requests.get("http://localhost:8080/api/user/get")
        self.assertEqual(response2.status_code, 400)

    def test_get_user_fails_with_invalid_input(self):
        response2 = requests.get("http://localhost:8080/api/user/get?name=hahaha")
        self.assertEqual(response2.status_code, 400)

    def test_modify_user_fail_with_missing_input(self):
        response2 = requests.put('http://localhost:8080/api/user/edit', data='{"userName": "vacuum", "userPassword": "134"}')
        self.assertEqual(response2.status_code, 400)

    def test_delete_user_fail_with_invalid_input(self):
        response2 = requests.post('http://localhost:8080/api/user/delete', data='{"userName": "vacuum"}')
        self.assertEqual(response2.status_code, 400)

    def test_get_chores_for_a_particular_user_in_a_particular_group_fail_with_invalid_input(self):
        response2 = requests.get('http://localhost:8080/api/user/get-unfinisihed-chores', data='{"userName": "hahaha"}')
        self.assertEqual(response2.status_code, 400)

    def test_validate_password_fail_with_missing_input(self):
        response2 = requests.post('http://localhost:8080/api/user', data='{"password": "123"}')
        self.assertEqual(response2.status_code, 400)

    def test_validate_password_with_correct_passowrd_and_user_email(self):
        response2 = requests.post('http://localhost:8080/api/user/validate-password',data='{"email": "michael@ucla.edu","password": "123"}')
        data = response2.json()
        self.assertEqual(data["result"], "true")

    def test_validate_password_with_incorrect_passowrd(self):
        response2 = requests.post('http://localhost:8080/api/user/validate-password',data='{"email": "michael@ucla.edu","password": "11123"}')
        data = response2.json()
        self.assertEqual(data["result"], "false")


if __name__ == '__main__':
    unittest.main()