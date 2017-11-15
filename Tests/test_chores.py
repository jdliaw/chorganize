import unittest
import sys
sys.path.append('..')
from database_setup import db, User, Group, createApp
import requests

class TestChores(unittest.TestCase):
    def setUp(self):
        app = createApp(True)
        app.app_context().push()
        db.create_all()
        self.addUserToDB()
        self.addGroupToDB()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def addUserToDB(self):
        user_obj = User(email="kchan52@ucla.edu", username="kaitlyne", password="hello", firstName="Kaitlyne", lastName="Chan")
        db.session.add(user_obj)
        db.session.commit()
        
    def addGroupToDB(self):
        group = Group(name="My Apartment")
        db.session.add(group)
        db.session.commit()
    
    def test_create_chore(self):
        response = requests.post('http://localhost:8080/api/chore/create', data='{"name": "vacuum", "groupID": 1}')
        self.assertEqual(response.status_code, 200)
        
    def test_create_chore_invalid(self):
        response = requests.post('http://localhost:8080/api/chore/create', data='{"name": "clean bathroom"}')
        self.assertGreaterEqual(response.status_code, 400)
        
if __name__ == '__main__':
    unittest.main()
