import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys
sys.path.append('..')
from database_setup import db, User, Group, Chore, createApp
print(str(id(db)) + "from database_setup importing this db")
#from backend import app, initApp
import requests

"""
class db
    def getUser
            json sdfdjkfhjdshfd
            return json;"""
class TestChores(unittest.TestCase):
    def setUp(self):
        app = createApp(True)
        app.app_context().push()
        db.create_all()
        app.testing = True
        #self.client = app.test_client()
        self.addUserToDB()
        self.addGroupToDB()
      
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
        
    def addUserToDB(self):
        user_obj = User(email="kchan52@ucla.edu", username="kaitlyne", password="hello", firstName="Kaitlyne", lastName="Chan")
        db.session.add(user_obj)
        db.session.commit()
        print("adding user")
        
    def addGroupToDB(self):
        group = Group(name="My Apartment")
        db.session.add(group)
        db.session.commit()
        print("adding group")
        
        chore = Chore(name="clean")
        group.addChore(chore)
    
    def test_create_chore(self):
        #response = self.client.post('/api/chore/create', data={"name": "vacuum", "groupID": 1})
        #print("response.data = " + str(response.data))
        #self.assertEqual(response.status_code, 200)
        response = requests.post('http://localhost:8080/api/chore/create', data='{"name": "vacuum", "groupID": 1}')
        print("response.data = " + response.text)
        self.assertEqual(response.status_code, 200)
        """
        response = requests.get('http://localhost:8080/api/chore/get?id=1')
        print("getting response.data = " + response.text)
        print("getting response.status_code = " + str(response.status_code))"""
        
if __name__ == '__main__':
    unittest.main()
