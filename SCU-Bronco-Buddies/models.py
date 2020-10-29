# create a class each database table we need
from init import db, bcrypt
from flask_login import UserMixin


# def init_db():
#     db.create_all()

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# a user can own multiple threads 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    threads = db.relationship('Thread', backref='owner')

    __abstract__ = True

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

	__abstract__ = True

# one forum has multiple threads 
class Forum(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	numThreads = db.Column(db.Integer, nullable=False)
	title = db.Column(db.String(100), nullable=False)
	description = db.Column(db.String(20), nullable=False)
	threads = db.relationship('Thread', backref='ForumType')

	__abstract__ = True
