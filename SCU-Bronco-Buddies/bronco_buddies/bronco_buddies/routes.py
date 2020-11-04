# routes.py - defining url paths 
from flask import render_template, request, url_for, flash, redirect # import the Flask class
from bronco_buddies import app, db, bcrypt
from bronco_buddies.models import User, Thread
from bronco_buddies.forms import RegistrationForm, LoginForm, NewPostForm
from flask_login import login_user, current_user, logout_user, login_required
from flask import escape
import jinja2

# home page 
@app.route("/")
@app.route("/home")
def home():
    posts = Thread.query.all()
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

#create a post
@app.route("/post/new", methods=['GET', 'POST'])
#@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        post = Thread(title=form.title.data, body=form.content.data, upvotes=0, downvotes=0, status="test", owner_id=current_user.firstname+" "+current_user.lastname, forum_id=1)
        db.session.add(post)
        db.session.commit() 
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    print(form.errors)
    return render_template('create_post.html', title='New Post', form=form)

#post view
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Thread.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

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