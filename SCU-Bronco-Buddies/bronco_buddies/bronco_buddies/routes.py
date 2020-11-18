# routes.py - defining url paths 
from flask import render_template, request, url_for, flash, redirect, abort # import the Flask class
from bronco_buddies import app, db, bcrypt
from bronco_buddies.models import User, Forum, Thread, Reply
from bronco_buddies.forms import RegistrationForm, LoginForm, NewPostForm, NewForumForm, ReplyForm
from flask_login import login_user, current_user, logout_user, login_required
from flask import escape
import jinja2

# home page 
@app.route("/")
@app.route("/home")
def home():
    posts = Thread.query.all()
    return render_template('home.html', title='Home', posts=posts)

@app.route("/")
@app.route("/landing")
def landingPage():
    return render_template('landing.html', title='Home')

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


#create a new post
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        # save to database 
        print(form.forumType.data.id)
        post = Thread(title=escape(form.title.data), body=escape(form.content.data), votes=0, status="OPEN", 
                                    owner_id=current_user.id, forum_id=form.forumType.data.id) # forum_id=form.forum_type.data

        # increment numThreads counter for the chosen forum 
        forum = Forum.query.filter_by(id=form.forumType.data.id).first()
        forum.numThreads += 1
        # how to save value in 

        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('post', post_id=post.id))
    else: 
         flash('There was an error! Please try again.', 'danger')
    return render_template('create_post.html', title='New Post', 
        form=form, legend='New Post')


#view post
@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Thread.query.get_or_404(post_id)
    poster = User.query.filter_by(id=post.owner_id).first()

    replies = Reply.query.filter_by(thread_id = post.id)
    names = []
    for reply in replies:
        user = User.query.filter_by(id=reply.owner_id).first()
        names.append(user.firstname + " " + user.lastname)
        print(names)
    form=ReplyForm()
    if form.validate_on_submit():
        reply = Reply(owner_id=current_user.id, body=escape(form.body.data), votes=0, thread_id=post_id)
        db.session.add(reply)
        db.session.commit()
        return redirect(url_for('post', post_id=post.id))
    return render_template('post.html', title=post.title, post=post, replies=replies, form=form, poster=poster)


#update posts
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Thread.query.get_or_404(post_id)
    # if post.author != current_user:
    #     abort(403)
    form = NewPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.content.data
        post.forum_id = form.forumType.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.body
        # form.forumType.data = post.forum_id
    return render_template('create_post.html', title='Update Post', form=form, 
        legend='Update Post')


#delete post
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Thread.query.get_or_404(post_id)
    # if post.author != current_user:
    #     abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

# profile page 
@app.route("/profile")
@login_required
def profile():
    user = current_user
    posts = Thread.query.filter_by(owner_id=current_user.id).all()
    for post in posts:
        print(post.title)
    # userpref = UserPref.query.filter_by(user_id = user.id).first()
    return render_template('profile.html', title='Profile', posts=posts)

@app.route("/admin")
@login_required
def admin():
    users = User.query.all()
    forums = Forum.query.all()
    return render_template('adminSettings.html', title='Admin Settings', users=users, forums=forums)

@app.route("/forum/add", methods=['GET', 'POST'])
@login_required
def add_forum():
    form = NewForumForm()
    forums = Forum.query.all()
    if form.validate_on_submit():
        # this isn't wrking, idk why. I think it doesn't like numThreads. 
        # forum = Forum(title=form.title, description=form.description)
        aform=Forum(numThreads=escape(0), title=escape(form.title.data), description=escape(form.description.data))
        db.session.add(aform)
        db.session.commit()
        return redirect(url_for('admin'))
    else: 
         flash('There was an error! Please try again.', 'danger')
    return render_template('create_forum.html', title="New Forum", form=form)

# logout 
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


# Upvote a reply 
@app.route("/upvote/<int:reply_id><int:post_id>", methods=['GET','POST'])
def upvoteReply(reply_id,post_id):
    curr_reply = Reply.query.filter_by(id=reply_id).first()
    curr_reply.votes += 1
    db.session.commit()
    return redirect(url_for('post', post_id=post_id))

# Downvote a reply
@app.route("/downvote/<int:reply_id><int:post_id>", methods=['GET','POST'])
def downvoteReply(reply_id,post_id):
    curr_reply = Reply.query.filter_by(id=reply_id).first()
    curr_reply.votes -= 1
    db.session.commit()
    return redirect(url_for('post', post_id=post_id))

# Upvote a thread
@app.route("/upvote/<int:post_id>", methods=['GET','POST'])
def upvotePost(post_id):
    curr_post = Thread.query.filter_by(id=post_id).first()
    curr_post.votes += 1
    db.session.commit()
    return redirect(url_for('post', post_id=post_id))

# downvote a thread
@app.route("/downvote/<int:post_id>", methods=['GET','POST'])
def downvotePost(post_id):
    curr_post = Thread.query.filter_by(id=post_id).first()
    curr_post.votes -= 1
    db.session.commit()
    return redirect(url_for('post', post_id=post_id))
