from . import routes
from flask import request
from database_setup import User, Group
from flask.json import loads, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

@routes.route('/api/user', methods=['POST'])
def createUser():
    """
    Create a new user and add to the database.
    
    :param email: the email of the user
    :param username: the username of the user
    :param password: the password of the user
    :param firstName: the first name of the user 
    :param lastName: the last name of the user
    
    :type email: str
    :type username: str
    :type password: str
    :type firstName: str
    :type lastName: str
    
    :return: "User Successfully Created", status code
    :rtype: str, int
    
    :raises KeyError: if the input is not provided by the user
    :raises sqlalchemy.exc.IntegrityError: if the user already existed in the database 
    """
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
    """
    Get information about a user.
    
    :param email: the email of the user
    :type email: str
    :return: a user JSON object, status code
    :rtype: JSON object, int
    :raises sqlalchemy.orm.exc.NoResultFound: if the user is not found in the database 
    """
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



#Edit User
@routes.route('/api/user', methods=['PUT'])
def modifyUser():
    """
    Modify fields of a User object.
    
    :param newemail: the new email of the user
    :param oldemail: the original email of the user
    :param username: the new username of the user
    :param password: the new password of the user
    :param firstName: the new firstName of the user
    :param lastName: the new lastName of the user
    
    :type newemail: str
    :type oldemail: str
    :type username: str
    :type password: str
    :type firstName: str
    :type lastName: str
    
    :return: "Successfully Modified", status code
    :rtype: str, int
    
    :raises KeyError: if the input is not provided by the user
    """
    data = request.data
    dataDict = loads(data)
    try:
        usernewEmail = dataDict['newemail']
        useroldEmail = dataDict['oldemail']
        userName = dataDict['username']
        userPassword = dataDict['password']
        userFirstName = dataDict['firstName']
        userLastName = dataDict['lastName']
    except KeyError:
        error = "Invalid input Parameters"
        return error, 400

    user = User.query.filter_by(email=useroldEmail).one()
    user.setEmail(usernewEmail)
    user.setPassword(userPassword)
    user.setFirstname(userFirstName)
    user.setLastname(userLastName)
    user.setUsername(userName)

    return "Successfully Modified"



#Delete User
@routes.route('/api/user/delete', methods=['POST'])
def deleteUser():
    """
    Delete a user from the database.
    
    :param email: the email of the user
    :type email: str
    :return: "User Successfully Removed", status code
    :rtype: str, int
    :raises KeyError: if the input is not provided by the user
    :raises sqlalchemy.orm.exc.NoResultFound: if the user is not found in the database 
    """
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

    return "User Successfully Removed"



#Get all active chores or completed chores for a particular user in a particular group
@routes.route('/api/user/getUnfinisihedChores', methods=['GET'])
def getChores():
    """
    Get all active chores or completed chores for a particular user in a particular group.
    
    :param email: the email of the user
    :param groupID: a particular groupID that the user is in
    :param completed: a boolean indicating whether a list of active chores or completed chores get return 
    
    :type email: str
    :type groupID: int
    :type completed: boolean
    
    :return: a list of JSON chore objects, status code
    :rtype: list of JSON objects, int
    
    :raises ValueError: if the input of the completed parameter is neither true or false
    :raises sqlalchemy.orm.exc.NoResultFound: if the user is not found in the database 
    """
    userEmail = request.args.get('email')
    groupID = request.args.get('groupID')
    completed = request.args.get('completed')
    try:
        completed = loads(completed.lower())
    except ValueError:
        error = "Input Format Error"
        return error, 400

    if userEmail is None or groupID is None:
        error = "Invalid input Parameters"
        return error, 400
    try:
        group = Group.getGroup(groupID)
    except NoResultFound:
        error = "Group Not Found"
        return error, 404

    activeChoreList = []
    completedChoreList = []
    choreList = group.getChores()
    resultList = []

    for chore in choreList:
        if chore.getUserEmail() == userEmail and chore.getCompleted() == False:
            activeChoreList.append(chore)
        elif chore.getUserEmail() == userEmail and chore.getCompleted() == True:
            completedChoreList.append(chore)

    if completed == False:
        resultList.append([chore.serialize for chore in completedChoreList])
    elif completed == True:
        resultList.append([chore.serialize for chore in activeChoreList])

    return jsonify(Chorelist=resultList)