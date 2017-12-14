from . import routes
from flask import request
from database_setup import User, Group, db
from flask.json import loads, jsonify
from sqlalchemy.orm.exc import NoResultFound

@routes.route('/api/group/create', methods=['POST'])
def create():
    """
    Create a new group and add it to the database. The user who created the group is automatically added as a member.
    
    :param email: the user's email
    :param groupName: the intended name for the group
    
    :type email: str
    :type groupName: str
    
    :return: a message that marks the success of creating the group, status code
    :rtype: str, int
    
    :raises KeyError: when lack of required fields of inputs
    :raises sqlalchemy.orm.exc.NoResultFound: when the user does not exist in the database
    """
    data = request.data
    dataDict = loads(data)
    try:
        email = dataDict['email']
        groupName = dataDict['groupName']
    except KeyError:
        error = "Lack Input Parameters"
        return error, 400

    try:
        user = User.getUser(email)
    except NoResultFound:
        error = "User Not Found"
        return error, 404

    group = Group.createGroup(groupName)
    group.addUser(user)

    return "Group Successfully Created"

@routes.route('/api/group/get-by-id', methods=['GET'])
def getByID():
    """
    Get information about a group, using the group's ID.
    
    :param groupID: the group's ID
    :type groupID: int
    :return: a JSON object that describes the group, status code
    :rtype: json, int
    :raises sqlalchemy.orm.exc.NoResultFound: when the group does not exist in database
    """
    groupID = request.args.get('groupID')
    try:
        group = Group.getGroup(groupID)
    except NoResultFound:
        error = "Group Not Found"
        return error, 404

    return jsonify(group.serialize)

@routes.route('/api/group/get-by-email', methods=['GET'])
def getByEmail():
    """
    Get a list of groups that a user is in.
    
    :param email: the user's email
    :type email: str
    :return: a JSON object that contains the descriptions of a list of groups, status code
    :rtype: json, int
    :raises sqlalchemy.orm.exc.NoResultFound: when the user does not exist in database
    """
    email = request.args.get('email')
    try:
        user = User.getUser(email)
    except NoResultFound:
        error = "User Not Found"
        return error, 404

    groups = user.getGroups()
    return jsonify(groups=[group.serialize for group in groups])

@routes.route('/api/group/edit', methods=['PUT'])
def edit():
    """
    Edit a group's name.
    
    :param groupID: the group's ID
    :param groupName: the intended new name for the group.
    
    :type groupID: int
    :type groupName: str
    
    :return: a message that marks the success of editing the group name, status code
    :rtype: str, int
    
    :raises KeyError: when lack of required fields of inputs
    :raises sqlalchemy.orm.exc.NoResultFound: when the group does not exist in database
    """
    data = request.data
    dataDict = loads(data)
    try:
        groupID = dataDict['groupID']
        groupName = dataDict['groupName']
    except KeyError:
        error = "Lack Input Parameters"
        return error, 400

    try:
        group = Group.getGroup(groupID)
    except NoResultFound:
        error = "Group Not Found"
        return error, 404

    group.setName(groupName)
    return "Group Name Successfully Edited"

@routes.route('/api/group/add-users', methods=['PUT'])
def addUsers():
    """
    Add users to a group.
    
    :param groupID: the group's ID
    :param listOfEmails: the list of user's emails waiting to be added to the group
    
    :type groupID: int
    :type listOfEmails: list of str
    
    :return: a message that marks the success of adding members to the group, status code
    :rtype: str, int
    
    :raises KeyError: when lack of required fields of inputs
    :raises sqlalchemy.orm.exc.NoResultFound: when the group/user does not exist in database
    """
    data = request.data
    dataDict = loads(data)
    try:
        groupID = dataDict['groupID']
        listOfEmails = dataDict['listOfEmails']
    except KeyError:
        error = "Lack Input Parameters"
        return error, 400

    try:
        group = Group.getGroup(groupID)
    except NoResultFound:
        error = "Group Not Found"
        return error, 404

    for email in listOfEmails:
        try:
            user = User.getUser(email)
        except NoResultFound:
            error = "User " + email + " Not Found"
            return error, 404

        group.addUser(user)

    return "Users Successfully Added To The Group"

@routes.route('/api/group/get-users', methods=['GET'])
def getUsers():
    """
    Get all users from the specified group.

    :param groupID: the group's ID

    :type groupID: int

    :return: a JSON object that contains the profiles of a list of users, status code
    :rtype: json, int

    :raises sqlalchemy.orm.exc.NoResultFound: when the group/user does not exist in database
    """
    groupID = request.args.get('groupID')

    try:
        group = Group.getGroup(groupID)
    except NoResultFound:
        error = "Group Not Found"
        return error, 404

    users = group.getUsers()
    users = [user.serialize for user in users]

    return jsonify(users=users)

@routes.route('/api/group/remove-user', methods=['PUT'])
def removeUser():
    """
    Remove a user from the group.
    
    :param groupID: the group's ID
    :param email: the user's email
    
    :type groupID: int
    :type email: str
    
    :return: a message that marks the success of removing a member from the group, status code
    :rtype: str, int

    :raises KeyError: when lack of required fields of inputs
    :raises sqlalchemy.orm.exc.NoResultFound: when the group/user does not exist in database
    """
    data = request.data
    dataDict = loads(data)
    try:
        groupID = dataDict['groupID']
        email = dataDict['email']
    except KeyError:
        error = "Lack Input Parameters"
        return error, 400

    try:
        group = Group.getGroup(groupID)
    except NoResultFound:
        error = "Group Not Found"
        return error, 404

    try:
        user = User.getUser(email)
    except NoResultFound:
        error = "User " + email + " Not Found"
        return error, 404

    group.removeUser(user)
    if len(group.getUsers()) == 0:
        Group.deleteGroup(group.getID())

    return "User Successfully Removed From The Group"

@routes.route('/api/group/get-completed-or-incompleted-chores', methods=['GET'])
def getCompletedOrIncompletedChores():
    """
    Get a list of a group's completed or incomplete chores.
    
    :param groupID: the group's ID
    :param completed: whether to get incompleted or completed chores
    
    :type groupID: int
    :type completed: boolean
    
    :return: a JSON object that contains the descriptions of a list of chores, status code
    :rtype: json, int

    :raises sqlalchemy.orm.exc.NoResultFound: when the group does not exist in database
    """
    groupID = request.args.get('groupID')
    completed = request.args.get('completed')
    try:
        group = Group.getGroup(groupID)
    except NoResultFound:
        error = "Group Not Found"
        return error, 404

    try:
        completed = loads(completed.lower())
    except ValueError:
        error = "Input Format Error"
        return error, 400

    chores = group.getChores()
    chores = [chore.serialize for chore in chores if chore.getCompleted() == completed]

    return jsonify(chores=chores)

@routes.route('/api/group/get-performance-by-group-and-email', methods=['GET'])
def getPerformanceByGroupAndEmail():
    """
    Get the user's performance in the specified group.

    :param groupID: the group's ID
    :param email: the user's email

    :type groupID: int
    :type email: str

    :return: a JSON object that contains the user's performance in the specified group.
    :rtype: json, int

    :raises sqlalchemy.orm.exc.NoResultFound: when the group does not exist in database
    """
    groupID = request.args.get('groupID')
    email = request.args.get('email')

    try:
        group = Group.getGroup(int(groupID))
    except NoResultFound:
        error = "Group Not Found"
        return error, 404

    performance = group.getPerformanceByEmail(email)

    if performance is None:
        error = "User " + email + " never joined the group before."
        return error, 404

    return jsonify(performance)