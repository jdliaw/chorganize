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

**User**

Primary class representing a user in our application.

```
  email: string
  username: string
  password: string
  firstName: string
  lastName: string
```

**Group**

A user can belong to a group which specifies chores to be done for a group.

```
  id: int
  name: string
  Users: [Users]
```

**Chore**

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
```

Retriever information about a user

```python
"""
@param str email: The email of the user
@return: str "A user Json object"
@return 400 if the input is not provided by the user
@raise NoResultFound: if the user is not found in the database
"""
@routes.route('/api/user', methods=['GET'])
def getUser():
```

```python

Modify a user's information

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
@routes.route('/api/user', methods=['PUT'])
def modifyUser():
```

Delete a user

```python
"""
@param str email: The email of the user
@return: "User Successfully Removed"
@raise keyError: If the input is not provided by the user
@raise NoResultFound: if the user is not found in the database
"""
@routes.route('/api/user/delete', methods=['POST'])
def deleteUser():
```

Get all active chores for a user in a specific group

```python
"""
@param str email: The email of the user
@param str groupID: A particular groupID that the user is in
@param str completed: A boolean indicating whether a list of active chores or completed chores get return
@return: A list of Json chore object
@raise ValueError: If the input of the completed parameter is neither true or false
@raise NoResultFound: if the user is not found in the database
"""
@routes.route('/api/user/getUnfinisihedChores', methods=['GET'])
def getChores():
```

### Groups


```python

```

```python

```

```python

```

```python

```

```python

```

```python

```

### Chores

Create a chore

```python
"""
@param str name: name of the chore (e.g. "vacuum")
@param int groupID: the unique ID of the group where the chore will be added
@param str deadline: the date that the chore should be completed by (m/d/yyyy)
@param str description: more information about the chore
@param str userEmail: the email of the user who will be assigned to the chore
@return str: a message confirming that the chore was successfully created
@raise KeyError: name and/or groupID parameters were not specified
@raise NoResultFound: user or group does not exist
"""
@routes.route('/api/chore', methods=['POST'])
def createChore():
```

Get information about a chore by ID

```python
"""
@param int id: the unique ID corresponding to the target chore
@return json: a JSON object that contains information about the chore (description, deadline, etc.)
@raise NoResultFound: chore corresponding to the specified ID does not exist
"""
@routes.route('/api/chore', methods=['GET'])
def getChoreByID():
```

Modify information about a chore

```python
"""
@param int id: the unique ID corresponding to the target chore
@return str: a message confirming that the chore was successfully modified
@raise KeyError: chore ID was not specified
"""
@routes.route('/api/chore', methods=['PUT'])
def modifyChore():
```

Delete a chore

```python
"""
@param int id: the unique ID corresponding to the target chore
@return str: a message confirming that the chore was successfully deleted
@raise KeyError: chore ID was not specified
"""
@routes.route('/api/chore', methods=['DELETE'])
def deleteChore():
```
