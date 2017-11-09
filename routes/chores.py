from . import routes
from flask import request
from database_setup import Chore
from flask.json import loads, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from datetime import datetime

@routes.route('/api/chore', methods=['POST'])
def createChore():
    data = request.data
    dataDict = loads(data)
    choreName = dataDict['name']
    if 'deadline' in dataDict:
        choreDeadlineStr = dataDict['deadline']
        choreDeadline = datetime.strptime(choreDeadlineStr, "%m/%d/%Y")
    else:
        choreDeadline = None
    if 'description' in dataDict:
        choreDescription = dataDict['description']
    else:
        choreDescription = None
    
    try:
        Chore.createChore(choreName, choreDeadline, choreDescription)
    except IntegrityError as error:
        return error, 500
        
    return "Chore successfully created"

@routes.route('/api/chore', methods=['GET'])
def getChoreByID():
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

@routes.route('/api/chore', methods=['PUT'])    
def modifyChore():
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
        chore.setCompleted(choreCompleted)
    
    return "Chore successfully modified"
    
@routes.route('/api/chore', methods=['DELETE'])
def deleteChore():
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
