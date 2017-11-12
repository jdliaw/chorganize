from . import routes
from flask import request
from database_setup import User, Group, db
from flask.json import loads, jsonify
from sqlalchemy.orm.exc import NoResultFound

@routes.route('/api/group/create', methods=['POST'])
def create():
    """
    @param str email: the user's email.
    @param str groupName: the intended name for the group.
    @return str: a message that marks the success of creating the group.
    @raise KeyError: when lack of required fields of inputs.
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
    user.addGroup(group)

    return "Group Successfully Created"

@routes.route('/api/group/get-by-id', methods=['GET'])
def getByID():
    """
    @param str groupID: the group's ID.
    @return json: a json object that describes the group.
    @raise NoResultFound: when the group does not exist in database.
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
    @param str email: the user's email.
    @return json: a json object that contains the descriptions of a list of groups.
    @raise NoResultFound: when the user does not exist in database.
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
    @param str groupID: the group's ID.
    @param str groupName: the intended new name for the group.
    @return str: a message that marks the success of editing the group name.
    @raise KeyError: when lack of required fields of inputs.
    @raise NoResultFound: when the group does not exist in database.
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
    return "Group Name Successfully Editted"

@routes.route('/api/group/add-users', methods=['PUT'])
def addUsers():
    """
    @param str groupID: the group's ID.
    @param list-of-str listOfEmails: the list of user's emails waiting to be added to the group.
    @return str: a message that marks the success of adding members to the group.
    @raise KeyError: when lack of required fields of inputs.
    @raise NoResultFound: when the group/user does not exist in database.
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

@routes.route('/api/group/remove-user', methods=['PUT'])
def removeUser():
    """
    @param str groupID: the group's ID.
    @param str email: the user's email.
    @return str: a message that marks the success of removing a member from the group.
    @raise KeyError: when lack of required fields of inputs.
    @raise NoResultFound: when the group/user does not exist in database.
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
        Group.deleteGroup(group.getId())

    return "User Successfully Removed From The Group"

@routes.route('/api/group/get-completed-or-incompleted-chores', methods=['GET'])
def getCompletedOrIncompletedChores():
    """
    @param str groupID: the group's ID.
    @param bool completed: whether to get incompleted or completed chores.
    @return json: a json object that contains the descriptions of a list of chores.
    @raise KeyError: when lack of required fields of inputs.
    @raise NoResultFound: when the group does not exist in database.
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