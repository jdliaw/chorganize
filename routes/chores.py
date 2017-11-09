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
    except IntegrityError as err:
        return err, 500
        
    return "Chore successfully created"