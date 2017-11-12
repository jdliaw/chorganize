from . import routes
from flask import request
from database_setup import User, db, Group
from flask.json import loads, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

"""  
@param str email: The email of the user
@param str username: The username of the username
@param str password: The password of the user
@param str firstName: The firstName of the user 
@param str lastName: The lastName of the user
@return: str "User Successfully Created"
@raise KeyError: If the input is not provided by the user
@raise IntegrityError: If the user already existed in the database 
"""
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


"""  
@param str email: The email of the user
@return: str "A user Json object"
@return 400 if the input is not provided by the user
@raise NoResultFound: if the user is not found in the database 
"""
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



"""  
@param str newemail: The new email of the user
@param str oldemail: The original email of the user
@param str username: The new username of the user
@param str password: The new password of the user
@param str firstName: The new firstName of the user
@param str lastName: The new lastName of the user
@return: "Successfully Modified"
@raise keyError: If the input is not provided by the user
"""
#Edit User
@routes.route('/api/user', methods=['PUT'])
def modifyUser():
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
    db.session.commit()

    return "Successfully Modified"


"""  
@param str email: The email of the user
@return: "User Successfully Removed"
@raise keyError: If the input is not provided by the user
@raise NoResultFound: if the user is not found in the database 
"""
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

    return "User Successfully Removed"


"""  
@param str email: The email of the user
@param str groupID: A particular groupID that the user is in
@param str completed: A boolean indicating whether a list of active chores or completed chores get return 
@return: A list of Json chore object
@raise ValueError: If the input of the completed parameter is neither true or false
@raise NoResultFound: if the user is not found in the database 
"""
#Get all active chores or completed chores for a particular user in a particular group
@routes.route('/api/user/getUnfinisihedChores', methods=['GET'])
def getChores():
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