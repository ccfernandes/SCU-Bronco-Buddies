from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy #form to run queries
from flask_login import login_user, logout_user, login_required, LoginManager
from form import RegistrationForm, LoginForm, NewPostForm
from models import User
import os

app = Flask(__name__)
# SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = '123456789098765432135792468'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///intellivoUser.db' # chose your database

db = SQLAlchemy(app)


# users directed here upon login
#Zac: put your main home page html here
@app.route('/')
def home():
    return render_template('home.html')


# login page  
@app.route("/login", methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "123":
            flash("You have been logged in!")

        # user = User.query.filter_by(email=form.email.data).first()
        # if user and bcrypt.check_password_hash(user.password, form.password.data):
        #     login_user(user)
        #     next_page = request.args.get('next') # redirect to next page if it exits (user tried accessing and is now logging in)
        #     return redirect(next_page) if next_page else redirect(url_for('profile'))
        print("Form is validated!")
        return redirect(url_for("home"))
        # else:
        #     flash('Login unsucessful. Please check credentials.', 'danger')
    else:
        flash('Login unsucessful. Please check credentials.', 'danger')
        print("Form is invalid.")
        print(form.errors)
    return render_template('login.html', title='Login', form=form)


# register page 
@app.route("/register", methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # user = User(username=escape(form.firstname.data), email=escape(form.email.data),
        #             password=escape(hashed_password))
        # db.session.add(user)
        # db.session.commit()
        print("Form has been validated!!!!")
        flash('Your account has been created. You are now able to log in!', 'success')
        return redirect(url_for('login'))
    else: 
        print("Form not validating.")
        print(form.errors)
    return render_template('signup.html', title='Register', form=form)

@app.route("/post/new", methods=['GET', 'POST'])
#@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form)
