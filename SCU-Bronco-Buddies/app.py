from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import login_user, logout_user, login_required
from models import User

app = Flask(__name__)

# users directed here upon login
#Zac: put your main home page html here
@app.route('/')
def home():
    return render_template('home.html')


# # login page  
# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     form=LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             login_user(user)
#             next_page = request.args.get('next') # redirect to next page if it exits (user tried accessing and is now logging in)
#             return redirect(next_page) if next_page else redirect(url_for('profile'))
#         else:
#             flash('Login unsucessful. Please check credentials.', 'danger')
#     return render_template('templates.html', title='Login', form=form)


# register page 
@app.route("/register", methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('user'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=escape(form.firstname.data), lastname=escape(form.lastname.data), email=escape(form.email.data),
                    password=escape(hashed_password))
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You are now able to log in!', 'success')
        return redirect(url_for('login'))
    return render_template('templates.html', title='Register', form=form)
