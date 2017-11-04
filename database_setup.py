from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chorganizer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


association_table = db.Table('users',
    db.Column('user_email', db.String(80), db.ForeignKey('user.email'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True),
)


class User(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(80), primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    total = db.Column(db.Integer, default=0)
    miss = db.Column(db.Integer, default=0)
    chores = db.relationship('Chore', backref='user', lazy='dynamic')

    def __init__(self, email, username, password, total=0, miss=0):
        self.email = email
        self.username = username
        self.password = password
        self.total = total
        self.miss = miss

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email
        db.session.commit()

    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username
        db.session.commit()

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password
        db.session.commit()

    def get_total(self):
        return self.total

    def set_total(self, total):
        self.total = total
        db.session.commit()

    def get_miss(self):
        return self.miss

    def set_miss(self, miss):
        self.miss = miss
        db.session.commit()

    def add_chore(self, chore):
        self.chores.append(chore)

    def get_chores(self):
        return self.chores.all()

    def get_chore_by_name(self, name):
        pass

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).one()

    @property
    def serialize(self):
        return {
                'email': self.email,
                'username': self.username,
                'password': self.password,
                'total': self.total,
                'misses': self.miss
               }


class Group(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    chores = db.relationship('Chore', backref='group', lazy='dynamic')
    users = db.relationship('User', secondary=association_table, lazy='subquery',
                            backref=db.backref('groups', lazy=True))
    """
    created = db.Column(db.DateTime, nullable=False,
                        server_default=db.func.now())

    user = db.relationship(
                          'User',
                          backref=db.backref('items', order_by=name.desc())
                          )
    """
    def __init__(self, name):
        self.name = name

    def get_id(self):
        return self.id

    def get_name(self):
        print self.name

    def set_name(self, name):
        self.name = name
        db.session.commit()

    def add_chore(self, chore):
        self.chores.append(chore)

    @property
    def serialize(self):
        return {
                'name': self.name,
                'user_email': self.user_email
               }


class Chore(db.Model):
    __tablename__ = 'chore'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    user_email = db.Column(db.String, db.ForeignKey('user.email'))

    def __init__(self, name):
        self.name = name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        db.session.commit()

    @property
    def serialize(self):
        return {
                'name': self.name,
                'group_id': self.group_id,
                'user_email': self.user_email
               }

db.create_all()
