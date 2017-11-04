from database_setup import db, User, Group, Chore

user = User(email='fuck@gmail.com', username="shit", password="fuck")
group = Group(name="UCLA")
chore = Chore(name="cleaning")

db.session.add(user)
db.session.add(group)
db.session.add(chore)

user.add_chore(chore)
group.add_chore(chore)

db.session.commit()

user_2 = User.query.one()
group_2 = Group.query.one()
chore_1 = user_2.chores.one()
chore_2 = group_2.chores.one()
print chore_1.name
print chore_2.name

chores = user_2.get_chores()
print len(chores)