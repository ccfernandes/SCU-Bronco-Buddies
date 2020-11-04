# routes.py - defining url paths 
from flask import render_template, request, url_for, flash, redirect # import the Flask class
from bronco_buddies import app, db, bcrypt
from bronco_buddies.models import User
from bronco_buddies.forms import RegistrationForm, LoginForm, NewPostForm
from flask_login import login_user, current_user, logout_user, login_required
from flask import escape
import jinja2

# home page 
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')

# about page 
@app.route("/about")
def about():
    return render_template('about.html', title='About')

# register page 
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=escape(form.firstname.data), lastname=escape(form.lastname.data), email=escape(form.email.data),
                    password=escape(hashed_password))
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You are now able to log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
   
# login page  
@app.route("/login", methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next') # redirect to next page if it exits (user tried accessing and is now logging in)
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsucessful. Please check credentials.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/post/new", methods=['GET', 'POST'])
#@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form)

# profile page 
@app.route("/profile")
@login_required
def profile():
    user = current_user
    # userpref = UserPref.query.filter_by(user_id = user.id).first()
    return render_template('profile.html', title='Profile')

# logout 
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))