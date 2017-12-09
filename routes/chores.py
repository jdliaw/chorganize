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
    :param description: (optional) more information about the chore
    
    :type name: str
    :type groupID: int
    :type description: str
    
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
        
    chore = Chore.createChore(choreName, description=choreDescription, deadline=choreDeadline)
    group.addChore(chore)
        
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
    Modify the name and/or description of a chore.
    
    :param id: the unique ID corresponding to the target chore
    :param name: (optional) the new name for the chore
    :param description: (optional) the new description for the chore
    
    :type id: int
    :type name: str
    :type description: str
    
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
        
    if 'description' in dataDict:
        choreDescription = dataDict['description']
        chore.setDescription(choreDescription)
    
    return "Chore successfully modified"

@routes.route('/api/chore/assign', methods=['PUT'])
def assignUserOrDeadlineToChore():
    """
    Assign a user and/or deadline to a chore.
    
    Notes:
    For initial assignment, email and deadline are required parameters.
    For editing the deadline or assigned user later, email and deadline are optional parameters.
    Postcondition: both user and deadline must not be null.
    
    :param id: the unique ID corresponding to the target chore
    :param email: the email of the user who will be assigned to the chore
    :param deadline: the new deadline for the chore (format: "mm/dd/yyyy, HH:MM" with 24-hour clock)
    
    :type id: int
    :type email: str
    :type deadline: str
    
    :return: a message confirming that the user and deadline have been set, status code
    :rtype: str, int
    
    :raises KeyError: chore ID was not specified
    :raises sqlalchemy.orm.exc.NoResultFound: chore ID does not exist, or user email does not exist
    """
    data = request.data
    dataDict = loads(data)
    
    try:
        choreID = dataDict['id']
    except KeyError:
        error = "Chore ID not specified"
        return error, 400
        
    try:
        chore = Chore.getChore(choreID)
    except NoResultFound:
        error = "Chore not found"
        return error, 404

    chore.setCompleted(False)
        
    userEmail = None
    deadline = None
    
    if chore.userEmail is None and chore.deadline is None:
        try:
            userEmail = dataDict['email']
            deadline = dataDict['deadline']
        except KeyError:
            error = "Need to specify user email and deadline"
            return error, 400
    else:
        if 'email' in dataDict:
            userEmail = dataDict['email']
        if 'deadline' in dataDict:
            deadline = dataDict['deadline']
   
    if userEmail is not None:
        try:
            user = User.getUser(userEmail)
        except NoResultFound:
            error = "User not found"
            return error, 404
        user.addChore(chore)
        
    if deadline is not None:
        choreDeadlineStr = dataDict['deadline']
        choreDeadline = datetime.strptime(choreDeadlineStr, "%m/%d/%Y, %H:%M")
        chore.setDeadline(choreDeadline)
        
    return "User assignment and deadline set successfully"

@routes.route('/api/chore/complete', methods=['PUT'])
def completeChore():
    """
    User completes a chore.
    
    Precondition: chore must be assigned to a user and have a deadline.
    
    :param id: the unique ID corresponding to the target chore
    :type id: int
    
    :return: a message confirming that the chore was successfully completed, status code
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
    
    userEmail = chore.getUserEmail()
    if userEmail is None:
        error = "Chore is not assigned to a user"
        return error, 412
     
    deadline = chore.getDeadline()
    if deadline is None:
        error = "Chore does not have a deadline"
        return error, 412
      
    group = Group.getGroup(chore.getGroupID())
    group.incrementPerformanceTotalByEmail(userEmail)
    if not chore.deadlinePassed():
        group.incrementPerformanceOnTimeByEmail(userEmail)

    chore.setCompleted(True)
    chore.setDeadline(None)
    
    user = User.getUser(userEmail)
    user.removeChore(chore)
    
    return "Chore successfully completed"
    
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
