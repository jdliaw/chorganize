import unittest
import sys
sys.path.append('..')
from database_setup import createApp, db, User, Group, Chore
import requests
import json
import sqlalchemy.orm.exc

class TestChores(unittest.TestCase):
    def setUp(self):
        app = createApp(True)
        app.app_context().push()
        db.create_all()
        self.user = User.createUser("kchan52@ucla.edu", "kaitlyne", "hello", "Kaitlyne", "Chan")
        self.group = Group.createGroup("My Apartment")
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
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
       
    def test_create_chore_missing_input(self):
        response = requests.post('http://localhost:8080/api/chore/create', data='{"name": "clean bathroom"}')
        self.assertGreaterEqual(response.status_code, 400)
        
    def test_create_chore_more_input(self):
        response = requests.post('http://localhost:8080/api/chore/create',
                                 data='{"name": "sweep", "groupID": 1, "deadline": "11/20/2017, 23:59", "description": "sweep bedroom and living room", "userEmail": "kchan52@ucla.edu"}'
                                )
        self.assertEqual(response.status_code, 200)
        
        chore = Chore.getChore(1)
        choreName = chore.getName()
        groupID = chore.getGroupID()
        deadline = chore.getDeadline()
        description = chore.getDescription()
        userEmail = chore.getUserEmail()
        
        self.assertEqual(choreName, "sweep")
        self.assertEqual(groupID, 1)
        self.assertEqual(deadline.strftime('%m/%d/%Y'), "11/20/2017")
        self.assertEqual(description, "sweep bedroom and living room")
        self.assertEqual(userEmail, "kchan52@ucla.edu")
        
    def test_create_chore_invalid_input(self):
        response = requests.post('http://localhost:8080/api/chore/create',
                                 data='{"name": "take out trash", "groupID": 1, "userEmail": "idontexist@gmail.com"}'
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
            
        self.assertEqual(attributesPresent, True)
    
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
        response = requests.put('http://localhost:8080/api/chore/modify', data='{"id": 4, "deadline": "12/31/2017"}')
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
