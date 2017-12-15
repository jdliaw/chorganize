# chorganize
CS 130 Project Fall 2017

Hana Kim, Jennifer Liaw, Isaac Kim, Michael Shea, Yanting Zeng, Kaitlyne Chan

## Directory

`/routes`

Subdirectory containing all routes for HTTP methods being used in our API.

`/ChOrganizeApp`

Subdirectory containing all files for the iOS app portion of the project.

### Tests

`/ChOrganizeApp/ChOrganizeAppTests/`

`/ChOrganizeApp/ChOrganizeAppUITests/`

Subdirectories containing tests for iOS portion.

### Dependencies

`database_setup.py`

Flask and SQLAlchemy are included as libraries in the database setup.


## Class Structure

### User

Primary class representing a user in our application.

```
  email: string
  username:(Optional) string
  password: string
  firstName: string
  lastName: (Optional)string
```

### Group

A user can belong to a group which specifies chores to be done for a group.

```
  id: int
  name: string
  Users: [Users]
```

### Chore

Primary class representing chores as tasks to be completed.

```
  id: int
  name: string
  description: string
  completed: bool
  deadline: datetime
  groupID: int
  userEmail: string
  deadlinePassed: bool
```

## API Documentation

### Users

Create a user

```python
"""
Create a new user and add to the database, use Bcrypt to hash password

:param email: the email of the user
:param username: (optional) the username of the user
:param password: the password of the user
:param firstName: the first name of the user
:param lastName: (optional) the last name of the user

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
@routes.route('/api/user/create', methods=['POST'])
def createUser():
```

Retriever information about a user

```python
"""
Get information about a user.

:param email: the email of the user
:type email: str
:return: a user JSON object, status code
:rtype: JSON object, int
:raises sqlalchemy.orm.exc.NoResultFound: if the user is not found in the database
"""
@routes.route('/api/user/get', methods=['GET'])
def getUser():
```

Modify a user's information

```python
"""
Modify fields of a User object.

:param newemail: (optional) the new email of the user
:param oldemail: the original email of the user
:param username: (optional) the new username of the user
:param password: (optional) the new password of the user
:param firstName: (optional)the new firstName of the user
:param lastName: (optional) the new lastName of the user

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
@routes.route('/api/user/edit', methods=['PUT'])
def modifyUser():
```

Delete a user

```python
"""
Delete a user from the database.

:param email: the email of the user
:type email: str
:return: "User Successfully Removed", status code
:rtype: str, int
:raises KeyError: if the input is not provided by the user
:raises sqlalchemy.orm.exc.NoResultFound: if the user is not found in the database
"""
@routes.route('/api/user/delete', methods=['POST'])
def deleteUser():
```

Get all active chores for a user in a specific group

```python
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
@routes.route('/api/user/get-unfinished-chores', methods=['GET'])
def getChores():
```

Validate email and password when a user log in to the app.

```python
"""
Validate email and password when a user log in to the app.

:param email: the email of the user
:param password: password of a user

:type email: str
:type groupID: password

:return: Json with a result item, true/false
:rtype: Json object

:raises KeyError: if the input is not provided by the user
"""
@routes.route('/api/user/validate-password', methods=['POST'])
def validatePassword():
```

### Groups

Create a group

```python
"""
Create a new group and add it to the database. The user who created the group is automatically added as a member.

:param email: the user's email
:param groupName: the intended name for the group

:type email: str
:type groupName: str

:return: group ID, status code
:rtype: str, int

:raises KeyError: when lack of required fields of inputs
:raises sqlalchemy.orm.exc.NoResultFound: when the user does not exist in the database
"""
@routes.route('/api/group/create', methods=['POST'])
def create():
```

Get a group's information

```python
"""
Get information about a group, using the group's ID.

:param groupID: the group's ID
:type groupID: int
:return: a JSON object that describes the group, status code
:rtype: json, int
:raises sqlalchemy.orm.exc.NoResultFound: when the group does not exist in database
"""
@routes.route('/api/group/get-by-id', methods=['GET'])
def getByID():
```

Get the groups a user belongs to

```python
"""
Get a list of groups that a user is in.

:param email: the user's email
:type email: str
:return: a JSON object that contains the descriptions of a list of groups, status code
:rtype: json, int
:raises sqlalchemy.orm.exc.NoResultFound: when the user does not exist in database
"""
@routes.route('/api/group/get-by-email', methods=['GET'])
def getByEmail():
```

Edit a group's information

```python
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
@routes.route('/api/group/edit', methods=['PUT'])
def edit():
```

Add a user to a group

```python
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
@routes.route('/api/group/add-users', methods=['PUT'])
def addUsers():
```

Get users from a group

```python
"""
Get all users from the specified group.

:param groupID: the group's ID

:type groupID: int

:return: a JSON object that contains the profiles of a list of users, status code
:rtype: json, int

:raises sqlalchemy.orm.exc.NoResultFound: when the group/user does not exist in database
"""
@routes.route('/api/group/get-users', methods=['GET'])
def getUsers():
```

Remove a user

```python
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
@routes.route('/api/group/remove-user', methods=['PUT'])
def removeUser():
```

Get completed or incompleted chores

```python
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
@routes.route('/api/group/get-completed-or-incompleted-chores', methods=['GET'])
def getCompletedOrIncompletedChores():
```

Get the user's performance in the specified group

```python
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
@routes.route('/api/group/get-performance-by-group-and-email', methods=['GET'])
def getPerformanceByGroupAndEmail():
```

### Chores

Create a chore

```python
"""
Create a new Chore object and add it to the database.

:param name: name of the chore
:param groupID: the unique ID of the group where the chore will be added
:param description: (optional) more information about the chore

:type name: str
:type groupID: int
:type description: str

:return: chore ID, status code
:rtype: str, int

:raises KeyError: name or group ID was not specified
:raises sqlalchemy.orm.exc.NoResultFound: user or group does not exist
"""
@routes.route('/api/chore/create', methods=['POST'])
def createChore():
```

Get information about a chore

```python
"""
Get information about a chore.

:param id: the unique ID corresponding to the target chore
:type id: int

:return: a JSON object that contains information about the chore, status code
:rtype: JSON object, int

:raises sqlalchemy.orm.exc.NoResultFound: chore corresponding to the specified ID does not exist
"""
@routes.route('/api/chore/get', methods=['GET'])
def getChoreByID():
```

Modify name and description of a chore

```python
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
@routes.route('/api/chore/modify', methods=['PUT'])
def modifyChore():
```

Assign a chore to a user and set a deadline

```python
"""
Assign a user and/or deadline to a chore.

Notes:
For initial assignment, email and deadline are required parameters.
For editing the deadline or assigned user later, email and deadline are optional parameters.
Postcondition: both user and deadline must not be null.

:param id: the unique ID corresponding to the target chore
:param email: the email of the user who will be assigned to the chore
:param deadline: the new deadline for the chore (format: "mm/dd/yyyy")

:type id: int
:type email: str
:type deadline: str

:return: a message confirming that the user and deadline have been set, status code
:rtype: str, int

:raises KeyError: chore ID was not specified
:raises sqlalchemy.orm.exc.NoResultFound: chore ID does not exist, or user email does not exist
"""
@routes.route('/api/chore/assign', methods=['PUT'])
def assignUserOrDeadlineToChore():
```

Complete a chore

```python
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
@routes.route('/api/chore/complete', methods=['PUT'])
def completeChore():
```

Delete a chore

```python
"""
Delete a Chore object from the database.

:param id: the unique ID corresponding to the target chore
:type id: int

:return: a message confirming whether the chore was successfully deleted, status code
:rtype: str, int

:raises KeyError: chore ID was not specified
:raises sqlalchemy.orm.exc.NoResultFound: chore corresponding to the specified ID does not exist
"""
@routes.route('/api/chore/delete', methods=['DELETE'])
def deleteChore():
```


Examples
```
Create a user
POST
.../api/user/create
{
  "email": "abc11@gmail.com", 
  "firstName": "Pusheen11", 
  "lastName": "Code11",
  "password":"123",
  "username": "username11"
}
```
```
Create a group
POST
.../api/group/create
{
  "email": "abc11@gmail.com", 
  "groupName": "123"
}
```
```
Add a person to a group
PUT 
.../api/group/add-users
{
  "groupID": 1, 
  "listOfEmails" : ["abc11@gmail.com"]
}
```
```
Create a chore
POST
.../api/chore/create
{
  "name": "wash", 
  "groupID": 1
}
```
```
Assign a chore to a person
PUT
.../api/chore/assign
{
  "id": 1, 
  "email": "abc11@gmail.com",
  "deadline":"07/28/2020, 18:54"
}
```
