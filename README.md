# chorganize
CS 130 Project
Authors: Hana Kim, Jennifer Liaw, Isaac Kim, Michael Shea, Yanting Zeng, Kaitlyne Chan

### Directory

`/routes`
Subdirectory containing all routes for HTTP methods being used in our API.

`/ChOrganizeApp`
Subdirectory containing all files for the iOS app portion of the project.

`/ChOrganizeApp/ChOrganizeAppTests/`
`/ChOrganizeApp/ChOrganizeAppUITests/`
Subdirectories containing tests for iOS portion.

`database_setup.py`
Flask and SQLAlchemy are included as libraries in the databse setup.


### Class Structure

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

### API Documentation


