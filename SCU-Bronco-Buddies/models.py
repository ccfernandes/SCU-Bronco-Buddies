# create a class each database table we need
from init import db, bcrypt
from flask_login import UserMixin


def init_db():
    db.create_all()

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(40), nullable=False)
    lastname = db.Column(db.String(40))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.email}')"