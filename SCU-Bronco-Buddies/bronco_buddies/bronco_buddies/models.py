# definition of database tables 

from bronco_buddies import db, login_manager
from flask_login import UserMixin


def init_db():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(40), nullable=False)
    lastname = db.Column(db.String(40))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # pref = db.relationship('UserPref', backref='user', uselist=False) # one to one relationship

    threads = db.relationship('Thread', backref='owner')

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.email}')"


    # __abstract__ = True

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


# a user can have multiple threads 
# multiple threads can be part of a forum 
class Thread(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    upvotes = db.Column(db.Integer, nullable=False)
    downvotes = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(6), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id'))

    # __abstract__ = True

# one forum has multiple threads 
class Forum(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    numThreads = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(20), nullable=False)
    threads = db.relationship('Thread', backref='ForumType')


