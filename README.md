# chorganize
CS 130 Project Fall 2017

Hana Kim, Jennifer Liaw, Isaac Kim, Michael Shea, Yanting Zeng, Kaitlyne Chan

## Directory

`/routes`

Subdirectory containing all routes for HTTP methods being used in our API.

`/ChOrganizeApp`

Subdirectory containing all files for the iOS app portion of the project.

`/ChOrganizeApp/ChOrganizeAppTests/`

`/ChOrganizeApp/ChOrganizeAppUITests/`

Subdirectories containing tests for iOS portion.

`database_setup.py`

Flask and SQLAlchemy are included as libraries in the databse setup.


## Class Structure

**User**

```
  email: string
  username: string
  password: string
  firstName: string
  lastName: string
```

**Group**

```
  id: int
  name: string
  Users: [Users]
```

**Chore**

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

```python
"""
@param str email: The email of the user
@param str groupID: A particular groupID that the user is in
@param str completed: A boolean indicating whether a list of active chores or completed chores get return
@return: A list of Json chore object
@raise ValueError: If the input of the completed parameter is neither true or false
@raise NoResultFound: if the user is not found in the database
"""
#Get all active chores or completed chores for a particular user in a particular group
@routes.route('/api/user/getUnfinisihedChores', methods=['GET'])
def getChores():
```

### Groups

### Chores
