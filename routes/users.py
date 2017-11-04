from . import routes
from flask import request
from database_setup import User
from flask.json import loads, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

@routes.route('/api/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        data = request.data
        dataDict = loads(data)
        userEmail = dataDict['email']
        userName = dataDict['username']
        userPassword = dataDict['password']

        try:
            User.createUser(userEmail, userName, userPassword)
        except IntegrityError as e:
            err = str(e)
            if ("UNIQUE constraint failed: user.email" in err):
                return "User Exists"
            elif ("NOT NULL constraint failed: user.username" in err):
                return "Username None"
            elif ("NOT NULL constraint failed: user.password" in err):
                return "Password None"

        return "User Successfully Created"

    elif request.method == 'GET':
        userEmail = request.args.get('email')
        try:
            user = User.getUser(userEmail)
        except NoResultFound:
            return "User Not Found"

        return jsonify(user.serialize)