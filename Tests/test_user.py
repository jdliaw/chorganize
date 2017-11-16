import unittest
import requests
import sys
sys.path.append('..')
from database_setup import createApp, db, User, Group, Chore


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
        response2 = requests.put('http://localhost:8080/api/user/delete', data='{"email": "hello@ucla.edu}')
        self.assertEqual(response2.status_code, "User Successfully Removed")

    def test_get_user_fails_with_user_not_found(self):
        response2 = requests.get("http://localhost:8080/api/users?email=michael123@gmail.com")
        self.assertEqual(response2.status_code, 404)


    def test_get_user_fails_with_missing_input(self):
        response2 = requests.get("http://localhost:8080/api/user")
        self.assertEqual(response2.status_code, 400)

    def test_get_user_fails_with_invalid_input(self):
        response2 = requests.get("http://localhost:8080/api/user?name=hahaha")
        self.assertEqual(response2.status_code, 400)

    def test_modify_user_fail_with_missing_input(self):
        response2 = requests.put('http://localhost:8080/api/user', data='{"userName": "vacuum", "userPassword": "134"}')
        self.assertEqual(response2.status_code, 400)

    def test_delete_user_fail_with_invalid_input(self):
        response2 = requests.put('http://localhost:8080/api/user/delete', data='{"userName": "vacuum"}')
        self.assertEqual(response2.status_code, 400)

    def test_get_chores_for_a_particular_user_in_a_particular_group_fail_with_invalid_input(self):
        response2 = requests.get('http://localhost:8080/api/user/getUnfinisihedChores', data='{"userName": "hahaha"}')
        self.assertEqual(response2.status_code, 400)



if __name__ == '__main__':
    unittest.main()