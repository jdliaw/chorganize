from . import routes
from flask import request
from database_setup import db, User
from sqlalchemy.orm.exc import NoResultFound
from flask.json import jsonify
import json

@routes.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        data = request.data
        dataDict = json.loads(data)
        userEmail = dataDict['email']
        userName = dataDict['username']
        userPassword = dataDict['password']

        try:
            user = User.query.filter_by(email=userEmail).one()
        except NoResultFound:
            user = User(email=userEmail, username=userName, password=userPassword)
            db.session.add(user)
            db.session.commit()

        return json.dumps(request.json)

    elif request.method == 'GET':
        userEmail = request.args.get('email')
        print userEmail
        try:
            user = User.query.filter_by(email=userEmail).one()
        except NoResultFound:
            return "Not Found"

        return jsonify(user.serialize)


