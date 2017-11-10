from . import routes
from flask import request
from database_setup import User, db
from flask.json import loads, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

@routes.route('/api/user', methods=['POST'])
def createUser():
    data = request.data
    dataDict = loads(data)
    try:
        userEmail = dataDict['email']
        userName = dataDict['username']
        userPassword = dataDict['password']
        userFirstName = dataDict['firstName']
        userLastName = dataDict['lastName']
    except KeyError:
        error = "Invalid input Parameters"
        return error, 400

    try:
        User.createUser(userEmail, userName, userPassword, userFirstName, userLastName)
    except IntegrityError:
        error = "Failed to create new user"
        return error, 500

    return "User Successfully Created"


@routes.route('/api/user', methods=['GET'])
def getUser():
    userEmail = request.args.get('email')
    if userEmail is None:
        error = "Invalid input Parameters"
        return error, 400
    try:
        user = User.getUser(userEmail)
    except NoResultFound:
        error = "User Not found"
        return error, 404

    return jsonify(user.serialize)

# Edit
@routes.route('/api/user', methods=['PUT'])
def modifyUser():
    data = request.data
    dataDict = loads(data)
    try:
        usernewEmail = dataDict['newemail']
        useroldEmail = dataDict['oldemail']
        userName = dataDict['username']
        userPassword = dataDict['password']
        userFirstName = dataDict['firstname']
        userLastName = dataDict['lastname']
    except KeyError:
        error = "Invalid input Parameters"
        return error, 400

    user = User.query.filter_by(email=useroldEmail).one()
    user.setEmail(usernewEmail)
    user.setPassword(userPassword)
    user.setFirstname(userFirstName)
    user.setLastname(userLastName)
    user.setUsername(userName)
    db.session.commit()

    return "Successfully Modified"



#Delete User
@routes.route('/api/user/delete', methods=['POST'])
def deleteUser():
    data = request.data
    dataDict = loads(data)

    try:
        userEmail = dataDict['email']
    except KeyError:
        error = "Invalid input Parameters"
        return error, 400

    try:
        User.deleteUser(userEmail)
    except NoResultFound:
        error = "User Not found"
        return error, 404

    return "User Successfully Romved"