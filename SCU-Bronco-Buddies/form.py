from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username',
						validators=[DataRequired()])
	email = StringField('Email',
						validators=[DataRequired(), Email()])
	password = PasswordField('Password',
							validators=[DataRequired()])
	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	email = StringField('Email',
						validators=[DataRequired(), Email()])
	password = PasswordField('Password',
							validators=[DataRequired()])
	submit = SubmitField('Log In')

class NewPostForm(FlaskForm):
	title = StringField('Title',
						validators=[DataRequired()])
	content = StringField('Question Body',
						validators=[DataRequired()])
	username = StringField('Username',
						validators=[DataRequired()])
	# replace current choices with a query for all rows in forum table 
	forumType = SelectField('Question Type',
						validators=[DataRequired()],
						choices=[('1','On Campus'), ('2','Technology'), ('3','Random'), ('4','Homework')])
	submit = SubmitField('Post')