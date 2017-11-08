from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


association_table = db.Table('association_table',
    db.Column('user_email', db.String(80), db.ForeignKey('user.email'), nullable=False),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), nullable=False),
    db.PrimaryKeyConstraint('user_email', 'group_id')
)


class User(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(80), primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    chores = db.relationship('Chore', backref='user', lazy='dynamic')
    groups = db.relationship('Group', secondary=association_table, lazy='dynamic',
                             backref=db.backref('users', lazy='dynamic'))

    def __init__(self, email, username, password, firstname, lastname):
        self.email = email
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname

    def getEmail(self):
        return self.email

    def setEmail(self, email):
        self.email = email
        db.session.commit()

    def getUsername(self):
        return self.username

    def setUsername(self, username):
        self.username = username
        db.session.commit()

    def getPassword(self):
        return self.password

    def setPassword(self, password):
        self.password = password
        db.session.commit()

    def getFirstname(self):
        return self.firstname

    def setFirstname(self, firstname):
        self.firstname = firstname
        db.session.commit()

    def getLastname(self):
        return self.lastname

    def setLastname(self, lastname):
        self.lastname = lastname
        db.session.commit()

    def addChore(self, chore):
        self.chores.append(chore)
        db.session.commit()

    def getChores(self):
        return self.chores.all()

    def addGroup(self, group):
        self.groups.append(group)
        db.session.commit()

    def getGroups(self):
        return self.groups.all()

    @classmethod
    def createUser(cls, email, username, password, firstname, lastname):
        user = User(email, username, password, firstname, lastname)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def getUser(cls, email):
        return cls.query.filter_by(email=email).one()

    @classmethod
    def deleteUser(cls, email):
        user = cls.getUser(email)
        db.session.delete(user)
        db.session.commit()

    @property
    def serialize(self):
        return {
                'email': self.email,
                'username': self.username,
                'password': self.password,
                'firstname': self.firstname,
                'lastname': self.lastname
               }


class Group(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    chores = db.relationship('Chore', backref='group', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def getId(self):
        return self.id

    def getName(self):
        print self.name

    def setName(self, name):
        self.name = name
        db.session.commit()

    def addChore(self, chore):
        self.chores.append(chore)
        db.session.commit()

    def getChores(self):
        return self.chores.all()

    def addUser(self, user):
        self.users.append(user)
        db.session.commit()

    def getUsers(self):
        return self.users.all()

    def removeUser(self, user):
        self.users.remove(user)
        db.session.commit()

    @classmethod
    def createGroup(cls, name):
        group = Group(name)
        db.session.add(group)
        db.session.commit()
        return group

    @classmethod
    def getGroup(cls, id):
        return cls.query.filter_by(id=id).one()

    @classmethod
    def deleteGroup(cls, id):
        group = cls.getGroup(id)
        db.session.delete(group)
        db.session.commit()

    @property
    def serialize(self):
        return {
                'id': self.id,
                'name': self.name
               }


class Chore(db.Model):
    __tablename__ = 'chore'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, default=None)
    completed = db.Column(db.Boolean, default=False)
    deadline = db.Column(db.DateTime)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    user_email = db.Column(db.String, db.ForeignKey('user.email'))

    def __init__(self, name, deadline=None, description=None, completed=False):
        self.name = name
        self.deadline = deadline
        self.description = description
        self.completed = completed

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name
        db.session.commit()

    def getDeadline(self):
        return self.deadline

    def setDeadline(self, deadline):
        self.deadline = deadline
        db.session.commit()

    @classmethod
    def createChore(cls, name, deadline=None, description=None, completed=False):
        chore = Chore(name, deadline, description, completed)
        db.session.add(chore)
        db.session.commit()
        return chore

    @classmethod
    def getChore(cls, id):
        return cls.query.filter_by(id=id).one()

    @classmethod
    def deleteChore(cls, id):
        chore = cls.getChore(id)
        db.session.delete(chore)
        db.session.commit()

    @property
    def serialize(self):
        return {
                'name': self.name,
                'group_id': self.group_id,
                'user_email': self.user_email
               }

db.create_all()
