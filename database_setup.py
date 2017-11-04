from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chorganizer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

users = db.Table('users',
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
    chores = db.relationship('Chore', backref='user', lazy=True)

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
    user_email = db.Column(db.String, db.ForeignKey('user.email'))
    chores = db.relationship('Chore', backref='group', lazy=True)
    users = db.relationship('User', secondary=users, lazy='subquery',
                            backref=db.backref('groups', lazy=True))
    """
    created = db.Column(db.DateTime, nullable=False,
                        server_default=db.func.now())

    user = db.relationship(
                          'User',
                          backref=db.backref('items', order_by=name.desc())
                          )
    """

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

    @property
    def serialize(self):
        return {
                'name': self.name,
                'group_id': self.group_id,
                'user_email': self.user_email
               }

db.create_all()