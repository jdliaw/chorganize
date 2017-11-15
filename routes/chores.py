from . import routes
from flask import request
from database_setup import Chore, Group, User
from flask.json import loads, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

@routes.route('/api/chore/create', methods=['POST'])
def createChore():
    """
    Create a new Chore object.
    
    @param str name: name of the chore (e.g. "vacuum")
    @param int groupID: the unique ID of the group where the chore will be added
    @param str deadline: the date that the chore should be completed by (m/d/yyyy)
    @param str description: more information about the chore
    @param str userEmail: the email of the user who will be assigned to the chore
    
    @return str: a message confirming that the chore was successfully created
    
    @raise KeyError: name and/or groupID parameters were not specified
    @raise NoResultFound: user or group does not exist
    """
    data = request.data
    dataDict = loads(data)
    
    try:
        choreName = dataDict['name']
        groupID = dataDict['groupID']
    except KeyError:
        error = "Name or group ID not specified"
        return error, 400
        
    try:
        group = Group.getGroup(groupID)
    except NoResultFound:
        error = "Group not found"
        return error, 404
    
    if 'deadline' in dataDict:
        choreDeadlineStr = dataDict['deadline']
        choreDeadline = datetime.strptime(choreDeadlineStr, "%m/%d/%Y")
    else:
        choreDeadline = None
        
    if 'description' in dataDict:
        choreDescription = dataDict['description']
    else:
        choreDescription = None
        
    chore = Chore.createChore(choreName, description=choreDescription, deadline=choreDeadline)
    group.addChore(chore)
        
    if 'userEmail' in dataDict:
        userEmail = dataDict['userEmail']
        try:
            user = User.getUser(userEmail)
        except NoResultFound:
            error = "User not found"
            return error, 404
        user.addChore(chore)
        
    return "Chore successfully created"

@routes.route('/api/chore/get', methods=['GET'])
def getChoreByID():
    """
    Get information about a chore.
    
    @param int id: the unique ID corresponding to the target chore
    
    @return json: a JSON object that contains information about the chore (description, deadline, etc.)
    
    @raise NoResultFound: chore corresponding to the specified ID does not exist
    """
    choreID = int(request.args.get('id'))
    if choreID is None:
        error = "No ID specified"
        return error, 400
    try:
        chore = Chore.getChore(choreID)
    except NoResultFound:
        error = "Chore not found"
        return error, 404
        
    return jsonify(chore.serialize)

@routes.route('/api/chore/modify', methods=['PUT'])    
def modifyChore():
    """
    Modify fields of a Chore object.
    
    @param int id: the unique ID corresponding to the target chore
    
    @return str: a message confirming that the chore was successfully modified
    
    @raise KeyError: chore ID was not specified
    """
    data = request.data
    dataDict = loads(data)
    
    try:
        choreID = dataDict['id']
    except KeyError:
        error = "No ID specified"
        return error, 400
    
    chore = Chore.query.filter_by(id=choreID).one()
    if 'name' in dataDict:
        choreName = dataDict['name']
        chore.setName(choreName)
    if 'deadline' in dataDict:
        choreDeadlineStr = dataDict['deadline']
        choreDeadline = datetime.strptime(choreDeadlineStr, "%m/%d/%Y")
        chore.setDeadline(choreDeadline)
    if 'description' in dataDict:
        choreDescription = dataDict['description']
        chore.setDescription(choreDescription)
    if 'completed' in dataDict:
        choreCompleted = dataDict['completed']
        if not chore.getCompleted() and choreCompleted:
            group = Group.getGroup(chore.getGroupID())
            email = chore.getUserEmail()
            record = group.getUserPerformances()[email]
            record['total'] += 1
            if not chore.deadlinePassed():
                record['onTime'] += 1
        chore.setCompleted(choreCompleted)
    
    return "Chore successfully modified"
    
@routes.route('/api/chore/delete', methods=['DELETE'])
def deleteChore():
    """
    Delete a Chore object.
    
    @param int id: the unique ID corresponding to the target chore
    
    @return str: a message confirming that the chore was successfully deleted
    
    @raise KeyError: chore ID was not specified
    """
    data = request.data
    dataDict = loads(data)

    try:
        choreID = dataDict['id']
    except KeyError:
        error = "No ID specified"
        return error, 400

    try:
        Chore.deleteChore(choreID)
    except NoResultFound:
        error = "Chore not found"
        return error, 404

    return "Chore successfully removed"
