import unittest
import requests
from json import loads
import sys
sys.path.append('..')
from database_setup import createApp, db, User, Group, Chore

class TestGroup(unittest.TestCase):
    ClassIsSetup = False

    def setUp(self):
        if not self.ClassIsSetup:
            self.setupClass()
            self.__class__.ClassIsSetup = True

    def setupClass(self):
        app = createApp(True)
        app.app_context().push()
        db.create_all()
        self.user1 = User.createUser("zengyt94@ucla.edu", "Yanting", "hello", "Yanting", "Zeng")
        self.user2 = User.createUser("kchan52@ucla.edu", "Kaitlyne", "hello", "Kaitlyne", "Chan")
        self.user3 = User.createUser("hello@ucla.edu", "hello", "hello", "hello", "hello")
        self.user4 = User.createUser("hi@ucla.edu", "hi", "hi", "hi", "hi")
        self.addGroupToDB()
        self.addChoreToDB()

    def addGroupToDB(self):
        self.group1 = Group.createGroup("First Group")
        self.group2 = Group.createGroup("Second Group Old Name")
        self.group1.addUser(self.user1)
        self.group1.addUser(self.user3)
        self.group1.addUser(self.user4)
        self.group2.addUser(self.user1)
        self.group2.addUser(self.user2)
        self.group2.addUser(self.user4)

    def addChoreToDB(self):
        self.chore1 = Chore.createChore("Cleaning")
        self.chore2 = Chore.createChore("Sweeping", completed=True)
        self.chore3 = Chore.createChore("Tidying")
        self.group1.addChore(self.chore1)
        self.group1.addChore(self.chore2)
        self.group2.addChore(self.chore3)

    def test_create(self):
        json = {'email': 'zengyt94@ucla.edu', 'groupName': 'Third Group'}
        response = requests.post('http://localhost:8080/api/group/create', json=json)
        self.assertEqual(response.status_code, 200)

        group3 = Group.getGroup(3)
        self.assertEqual(group3.getName(), 'Third Group')

    def test_get_by_id(self):
        params = {'groupID': 1}
        response = requests.get('http://localhost:8080/api/group/get-by-id', params=params)
        self.assertEqual(response.status_code, 200)

        dataDict = loads(response.text)
        self.assertEqual(dataDict['name'], 'First Group')

    def test_get_by_email(self):
        params = {'email': 'hi@ucla.edu'}
        response = requests.get('http://localhost:8080/api/group/get-by-email', params=params)
        self.assertEqual(response.status_code, 200)

        dataDict = loads(response.text)
        self.assertEqual(len(dataDict['groups']), 2)

    def test_edit(self):
        json = {'groupID': 2, 'groupName': 'Second Group New Name'}
        response = requests.put('http://localhost:8080/api/group/edit', json=json)
        self.assertEqual(response.status_code, 200)

        group2 = Group.getGroup(2)
        self.assertEqual(group2.getName(), 'Second Group New Name')

    def test_add_users(self):
        json = {'groupID': 1, 'listOfEmails': ['kchan52@ucla.edu']}
        response = requests.put('http://localhost:8080/api/group/add-users', json=json)
        self.assertEqual(response.status_code, 200)

        user2 = User.getUser('kchan52@ucla.edu')
        self.assertEqual(user2.getGroups()[0].getName(), 'First Group')

    def test_get_users(self):
        params = {'groupID': 2}
        response = requests.get('http://localhost:8080/api/group/get-users', params=params)
        self.assertEqual(response.status_code, 200)

        dataDict = loads(response.text)
        self.assertEqual(len(dataDict['users']), 3)
        self.assertEqual(dataDict['users'][0]['firstName'], 'Yanting')
        self.assertEqual(dataDict['users'][1]['firstName'], 'Kaitlyne')
        self.assertEqual(dataDict['users'][2]['firstName'], 'hi')

    def test_remove_user(self):
        json = {'groupID': 1, 'email': 'hello@ucla.edu'}
        response = requests.put('http://localhost:8080/api/group/remove-user', json=json)
        self.assertEqual(response.status_code, 200)

        user3 = User.getUser('hello@ucla.edu')
        self.assertEqual(len(user3.getGroups()), 0)

    def test_get_completed_chores(self):
        params = {'groupID': 1, 'completed': 'False'}
        response = requests.get('http://localhost:8080/api/group/get-completed-or-incompleted-chores', params=params)
        self.assertEqual(response.status_code, 200)

        chore1 = Chore.getChore(1)
        self.assertEqual(chore1.getName(), 'Cleaning')

    def test_get_incompleted_chores(self):
        params = {'groupID': 1, 'completed': 'True'}
        response = requests.get('http://localhost:8080/api/group/get-completed-or-incompleted-chores', params=params)
        self.assertEqual(response.status_code, 200)

        chore2 = Chore.getChore(2)
        self.assertEqual(chore2.getName(), 'Sweeping')

    def test_get_performance_by_group_and_email(self):
        params = {'groupID': 2, 'email': 'zengyt94@ucla.edu'}
        response = requests.get('http://localhost:8080/api/group/get-performance-by-group-and-email', params=params)

        dataDict = loads(response.text)
        self.assertEqual(dataDict['total'], 0)
        self.assertEqual(dataDict['onTime'], 0)

        json = {'id': 3, 'email': 'zengyt94@ucla.edu', 'deadline': '12/23/2056, 23:59'}
        requests.put('http://localhost:8080/api/chore/assign', json=json)

        json = {'id': 3}
        requests.put('http://localhost:8080/api/chore/complete', json=json)

        params = {'groupID': 2, 'email': 'zengyt94@ucla.edu'}
        response = requests.get('http://localhost:8080/api/group/get-performance-by-group-and-email', params=params)

        dataDict = loads(response.text)
        self.assertEqual(dataDict['total'], 1)
        self.assertEqual(dataDict['onTime'], 1)

if __name__ == '__main__':
    unittest.main()

