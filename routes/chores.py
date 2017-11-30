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
    Create a new Chore object and add it to the database.
    
    :param name: name of the chore
    :param groupID: the unique ID of the group where the chore will be added
    :param deadline: (optional) the date that the chore should be completed by (format: "mm/dd/yyyy, HH:MM")
    :param description: (optional) more information about the chore
    :param userEmail: (optional) the email of the user who will be assigned to the chore
    
    :type name: str
    :type groupID: int
    :type deadline: str
    :type description: str
    :type userEmail: str
    
    :return: a message confirming whether the chore successfully created, status code
    :rtype: str, int
    
    :raises KeyError: name or group ID was not specified
    :raises sqlalchemy.orm.exc.NoResultFound: user or group does not exist
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
    
    if 'description' in dataDict:
        choreDescription = dataDict['description']
    else:
        choreDescription = None
    
    if 'deadline' in dataDict:
        choreDeadlineStr = dataDict['deadline']
        choreDeadline = datetime.strptime(choreDeadlineStr, "%m/%d/%Y, %H:%M")
    else:
        choreDeadline = None
        
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
    
    :param id: the unique ID corresponding to the target chore
    :type id: int
    
    :return: a JSON object that contains information about the chore, status code
    :rtype: JSON object, int
    
    :raises sqlalchemy.orm.exc.NoResultFound: chore corresponding to the specified ID does not exist
    """
    choreIDstr = request.args.get('id')
    if choreIDstr is None:
        error = "No ID specified"
        return error, 400
    choreID = int(choreIDstr)
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
    
    :param id: the unique ID corresponding to the target chore
    :param name: (optional) the new name for the chore
    :param deadline: (optional) the new deadline for the chore (format: "mm/dd/yyyy, HH:MM")
    :param description: (optional) the new description for the chore
    :param completed: (optional) whether the chore has been completed or not
    
    :type id: int
    :type name: str
    :type deadline: str
    :type description: str
    :type completed: boolean
    
    :return: a message confirming whether the chore was successfully modified, status code
    :rtype: str, int
    
    :raises KeyError: chore ID was not specified
    :raises sqlalchemy.orm.exc.NoResultFound: chore corresponding to the specified ID does not exist
    """
    data = request.data
    dataDict = loads(data)
    
    try:
        choreID = dataDict['id']
    except KeyError:
        error = "No ID specified"
        return error, 400
        
    try:
        chore = Chore.getChore(choreID)
    except NoResultFound:
        error = "Chore not found"
        return error, 404
    
    if 'name' in dataDict:
        choreName = dataDict['name']
        chore.setName(choreName)
        
    if 'deadline' in dataDict:
        choreDeadlineStr = dataDict['deadline']
        choreDeadline = datetime.strptime(choreDeadlineStr, "%m/%d/%Y, %H:%M")
        chore.setDeadline(choreDeadline)
        
    if 'description' in dataDict:
        choreDescription = dataDict['description']
        chore.setDescription(choreDescription)
        
    if 'completed' in dataDict:
        choreCompleted = dataDict['completed']
        if not chore.getCompleted() and choreCompleted:
            group = Group.getGroup(chore.getGroupID())
            email = chore.getUserEmail()

            group.incrementPerformanceTotalByEmail(email)
            if not chore.deadlinePassed():
                group.incrementPerformanceOnTimeByEmail(email)

        chore.setCompleted(choreCompleted)
    
    return "Chore successfully modified"
    
@routes.route('/api/chore/delete', methods=['DELETE'])
def deleteChore():
    """
    Delete a Chore object from the database.
    
    :param id: the unique ID corresponding to the target chore
    :type id: int
    
    :return: a message confirming whether the chore was successfully deleted, status code
    :rtype: str, int
    
    :raises KeyError: chore ID was not specified
    :raises sqlalchemy.orm.exc.NoResultFound: chore corresponding to the specified ID does not exist
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
