import unittest
import sys
sys.path.append('..')
from database_setup import createApp, db, User, Group, Chore
import requests
import json
import sqlalchemy.orm.exc
from datetime import datetime

class TestChores(unittest.TestCase):
    def setUp(self):
        db.create_all()
        self.user = User.createUser("kchan52@ucla.edu", "kaitlyne", "hello", "Kaitlyne", "Chan")
        self.group = Group.createGroup("My Apartment")
        self.group.addUser(self.user)
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    @classmethod
    def setUpClass(cls):
        app = createApp(True)
        app.app_context().push()
        
    def addChoreToDB(self, name):
        chore = Chore.createChore(name)
        self.group.addChore(chore)
    
    def test_create_chore(self):
        response = requests.post('http://localhost:8080/api/chore/create', data='{"name": "vacuum", "groupID": 1}')
        self.assertEqual(response.status_code, 200)
        
        chore = Chore.getChore(1)
        choreName = chore.getName()
        groupID = chore.getGroupID()
        
        self.assertEqual(choreName, "vacuum")
        self.assertEqual(groupID, 1)
        
    def test_create_chore_optional_input(self):
        response = requests.post('http://localhost:8080/api/chore/create',
                                 data='{"name": "sweep", "groupID": 1, "description": "sweep bedroom and living room"}'
                                )
        self.assertEqual(response.status_code, 200)
        
        chore = Chore.getChore(1)
        choreName = chore.getName()
        groupID = chore.getGroupID()
        description = chore.getDescription()
        
        self.assertEqual(choreName, "sweep")
        self.assertEqual(groupID, 1)
        self.assertEqual(description, "sweep bedroom and living room")
       
    def test_create_chore_missing_input(self):
        response = requests.post('http://localhost:8080/api/chore/create', data='{"name": "clean bathroom"}')
        self.assertGreaterEqual(response.status_code, 400)
        
    def test_create_chore_invalid_input(self):
        response = requests.post('http://localhost:8080/api/chore/create',
                                 data='{"name": "take out trash", "groupID": 1000}'
                                )
        self.assertGreaterEqual(response.status_code, 400)
        
    def test_get_chore(self):
        self.addChoreToDB("wash dishes")
        response = requests.get('http://localhost:8080/api/chore/get?id=1')
        self.assertEqual(response.status_code, 200)
        
        dataDict = json.loads(response.text)
        if "id" in dataDict and "groupID" in dataDict and "name" in dataDict and dataDict["name"] == "wash dishes":
            attributesPresent = True
        else:
            attributesPresent = False
            
        self.assertTrue(attributesPresent)
    
    def test_get_chore_missing_input(self):
        self.addChoreToDB("clean sink")
        response = requests.get('http://localhost:8080/api/chore/get')
        self.assertGreaterEqual(response.status_code, 400)
        
    def test_get_chore_invalid_input(self):
        self.addChoreToDB("clean shower")
        response = requests.get('http://localhost:8080/api/chore/get?id=5')
        self.assertGreaterEqual(response.status_code, 400)
        
    def test_modify_chore_name(self):
        self.addChoreToDB("vacuum")
        response = requests.put('http://localhost:8080/api/chore/modify', data='{"id": 1, "name": "vacuum bedroom"}')
        self.assertEqual(response.status_code, 200)
        
        chore = Chore.getChore(1)
        choreName = chore.getName()
        
        self.assertEqual(choreName, "vacuum bedroom")
        
    def test_modify_chore_missing_input(self):
        self.addChoreToDB("vacuum")
        response = requests.put('http://localhost:8080/api/chore/modify', data='{"name": "vacuum bedroom"}')
        self.assertGreaterEqual(response.status_code, 400)
        
    def test_modify_chore_invalid_input(self):
        self.addChoreToDB("vacuum")
        response = requests.put('http://localhost:8080/api/chore/modify', data='{"id": 4, "name": "vacuum bedroom"}')
        self.assertGreaterEqual(response.status_code, 400)
        
    def test_assign_chore(self):
        self.addChoreToDB("sweep")
        response = requests.put('http://localhost:8080/api/chore/assign', data='{"id": 1, "email": "kchan52@ucla.edu", "deadline": "12/31/2017, 23:55"}')
        self.assertEqual(response.status_code, 200)
        
        chore = Chore.getChore(1)
        userEmail = chore.getUserEmail()
        deadline = chore.getDeadline().strftime('%m/%d/%Y, %H:%M')
        completed = chore.getCompleted()
        
        self.assertEqual(userEmail, "kchan52@ucla.edu")
        self.assertEqual(deadline, "12/31/2017, 23:55")
        self.assertEqual(completed, False)
        
    def test_assign_chore_missing_input(self):
        self.addChoreToDB("sweep")
        response = requests.put('http://localhost:8080/api/chore/assign', data='{"id": 1, "deadline": "12/31/2017, 23:55"}')
        self.assertGreaterEqual(response.status_code, 400)
        
    def test_assign_chore_invalid_input(self):
        self.addChoreToDB("sweep")
        response = requests.put('http://localhost:8080/api/chore/assign', data='{"id": 100, "email": "kchan52@ucla.edu", "deadline": "12/31/2017, 23:55"}')
        self.assertGreaterEqual(response.status_code, 400)
        
    def test_complete_chore_on_time(self):
        self.addChoreToDB("sweep")
        chore = Chore.getChore(1)
        user = User.getUser("kchan52@ucla.edu")
        user.addChore(chore)
        deadline = datetime.strptime("12/12/2020, 12:12", "%m/%d/%Y, %H:%M")
        chore.setDeadline(deadline)
        
        response = requests.put('http://localhost:8080/api/chore/complete', data='{"id": 1}')
        self.assertEqual(response.status_code, 200)
        
        completed = chore.getCompleted()
        userEmail = chore.getUserEmail()
        deadline = chore.getDeadline()
        group = Group.getGroup(1)
        performance = group.getPerformanceByEmail("kchan52@ucla.edu")
        totalChores = performance["total"]
        onTimeChores = performance["onTime"]
        
        self.assertTrue(completed)
        self.assertIsNone(userEmail)
        self.assertIsNone(deadline)
        self.assertEqual(totalChores, 1)
        self.assertEqual(onTimeChores, 1)
        
    def test_complete_chore_late(self):
        self.addChoreToDB("sweep")
        chore = Chore.getChore(1)
        user = User.getUser("kchan52@ucla.edu")
        user.addChore(chore)
        deadline = datetime.strptime("11/30/2017, 23:59", "%m/%d/%Y, %H:%M")
        chore.setDeadline(deadline)
        
        response = requests.put('http://localhost:8080/api/chore/complete', data='{"id": 1}')
        self.assertEqual(response.status_code, 200)
        
        completed = chore.getCompleted()
        userEmail = chore.getUserEmail()
        deadline = chore.getDeadline()
        group = Group.getGroup(1)
        performance = group.getPerformanceByEmail("kchan52@ucla.edu")
        totalChores = performance["total"]
        onTimeChores = performance["onTime"]
        
        self.assertTrue(completed)
        self.assertIsNone(userEmail)
        self.assertIsNone(deadline)
        self.assertEqual(totalChores, 1)
        self.assertEqual(onTimeChores, 0)
        
    def test_complete_chore_missing_input(self):
        self.addChoreToDB("sweep")
        chore = Chore.getChore(1)
        user = User.getUser("kchan52@ucla.edu")
        user.addChore(chore)
        deadline = datetime.strptime("12/12/2020, 12:12", "%m/%d/%Y, %H:%M")
        chore.setDeadline(deadline)
        
        response = requests.put('http://localhost:8080/api/chore/complete', data='{}')
        self.assertGreaterEqual(response.status_code, 400)
        
    def test_complete_chore_invalid_input(self):
        self.addChoreToDB("sweep")
        chore = Chore.getChore(1)
        user = User.getUser("kchan52@ucla.edu")
        user.addChore(chore)
        deadline = datetime.strptime("12/12/2020, 12:12", "%m/%d/%Y, %H:%M")
        chore.setDeadline(deadline)
        
        response = requests.put('http://localhost:8080/api/chore/complete', data='{"id": 500}')
        self.assertGreaterEqual(response.status_code, 400)
        
    def test_delete_chore(self):
        self.addChoreToDB("dust shelves")
        response = requests.delete('http://localhost:8080/api/chore/delete', data='{"id": 1}')
        self.assertEqual(response.status_code, 200)       
        self.assertRaises(sqlalchemy.orm.exc.NoResultFound, Chore.getChore, 1)
        
    def test_delete_chore_missing_input(self):
        self.addChoreToDB("dust shelves")
        response = requests.delete('http://localhost:8080/api/chore/delete', data='{}')
        self.assertGreaterEqual(response.status_code, 400)
        
    def test_delete_chore_invalid_input(self):
        self.addChoreToDB("dust shelves")
        response = requests.delete('http://localhost:8080/api/chore/delete', data='{"id": 0}')
        self.assertGreaterEqual(response.status_code, 400)
        
if __name__ == '__main__':
    unittest.main()
