# routes.py - defining url paths 
from flask import render_template, request, url_for, flash, redirect, abort # import the Flask class
from bronco_buddies import app, db, bcrypt, mail
from bronco_buddies.models import User, Forum, Thread, Reply
from bronco_buddies.forms import RegistrationForm, LoginForm, UpdateAccountForm, NewPostForm, UpdatePostForm, NewForumForm, ReplyForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from flask import escape
from flask_mail import Message
import jinja2

# search page 
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Thread.query.paginate(page=page, per_page=20)
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
        form=form)




#view post
@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Thread.query.get_or_404(post_id)
    poster = User.query.filter_by(id=post.owner_id).first()
    replies = Reply.query.filter_by(thread_id = post.id)
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
    if post.owner_id != current_user.id:
        abort(403)
    form = UpdatePostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.content.data
        # post.forum_id = form.forumType.data]
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.body
        # form.forumType.data = post.forum_id
    return render_template('update_post.html', title='Update Post', form=form)


#delete post
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Thread.query.get_or_404(post_id)
    if post.owner_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

# profile page 
@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email
    posts = Thread.query.filter_by(owner_id=current_user.id).all()
    for post in posts:
        print(post.title)
    # userpref = UserPref.query.filter_by(user_id = user.id).first()
    return render_template('profile.html', title='Profile', posts=posts, form=form)


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
@app.route("/upvote/<reply_id>/<post_id>", methods=['GET','POST'])
def upvoteReply(reply_id,post_id):
    curr_reply = Reply.query.filter_by(id=reply_id).first()
    curr_reply.votes += 1
    db.session.commit()
    return redirect(url_for('post', post_id=post_id))

# Downvote a reply
@app.route("/downvote/<reply_id>/<post_id>", methods=['GET','POST'])
def downvoteReply(reply_id,post_id):
    curr_reply = Reply.query.filter_by(id=reply_id).first()
    curr_reply.votes -= 1
    db.session.commit()
    return redirect(url_for('post', post_id=post_id))

# Upvote a thread
@app.route("/upvote/<post_id>", methods=['GET','POST'])
def upvotePost(post_id):
    curr_post = Thread.query.filter_by(id=post_id).first()
    curr_post.votes += 1
    db.session.commit()
    return redirect(url_for('post', post_id=post_id))

# downvote a thread
@app.route("/downvote/<post_id>", methods=['GET','POST'])
def downvotePost(post_id):
    curr_post = Thread.query.filter_by(id=post_id).first()
    curr_post.votes -= 1
    db.session.commit()
    return redirect(url_for('post', post_id=post_id))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@broncobuddies.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


# request a password reset link
@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to rest your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated. You are now able to log in!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

