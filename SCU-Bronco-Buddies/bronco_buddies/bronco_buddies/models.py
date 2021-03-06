# definition of database tables 

from bronco_buddies import db, login_manager, app
from flask_login import UserMixin
from sqlalchemy.sql import func
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


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

    threads = db.relationship('Thread', backref='owner')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.email}')"


# a user can have multiple threads 
# multiple threads can be part of a forum 
# one thread has multiple replies
class Thread(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text(500), nullable=False)
    votes = db.Column(db.Integer, default=0)
    status = db.Column(db.String(6), nullable=False)
    date_posted = db.Column(db.DateTime(timezone=True), default=func.now())

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id')) # a thread belongs to a single user
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id')) # a thread belongs to a single forum
    replies = db.relationship('Reply', backref = 'reply_owner') # a thread can have multiple replies
    # __abstract__ = True

    def getForumTitle(self):
        return Forum.getTitleFromId(self.forum_id)


class Forum(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    numThreads = db.Column(db.Integer, default=0)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(500), nullable=False)

    # a forum has multiple threads 
    threads = db.relationship('Thread', backref='ForumType')

    def getTitleFromId(param_id):
        return Forum.query.filter_by(id=param_id).first().title


# we might need something to accept the answer accept=db.Column(db.Boolean)
class Reply(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text(500), nullable=False)
    votes = db.Column(db.Integer, default=0)
    date_posted = db.Column(db.DateTime(timezone=True), default=func.now())

    # a reply belongs to a single thread
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
    
