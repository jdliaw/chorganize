from . import routes
from flask import request
from database_setup import User, Group, db
from flask.json import loads, jsonify
from sqlalchemy.orm.exc import NoResultFound

@routes.route('/api/group/create', methods=['POST'])
def create():
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

@routes.route('/api/group/get_by_id/<string:groupID>', methods=['GET'])
def get_by_id(groupID):
    try:
        group = Group.getGroup(groupID)
    except NoResultFound:
        error = "Group Not Found"
        return error, 404

    return jsonify(group.serialize)

@routes.route('/api/group/get_by_email/<string:email>', methods=['GET'])
def get_by_email(email):
    try:
        user = User.getUser(email)
    except NoResultFound:
        error = "User Not Found"
        return error, 404

    groups = user.getGroups()
    return jsonify(groups=[group.serialize for group in groups])

@routes.route('/api/group/edit', methods=['PUT'])
def edit():
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

@routes.route('/api/group/addUsers', methods=['PUT'])
def addPeople():
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

@routes.route('/api/group/removeUser', methods=['PUT'])
def deletePeople():
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