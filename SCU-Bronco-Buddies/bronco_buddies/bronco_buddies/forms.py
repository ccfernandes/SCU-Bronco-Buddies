# definition of all forms in application 

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from bronco_buddies.models import User 


# registration form for login
class RegistrationForm(FlaskForm):
	firstname = StringField('Firstname', 
							validators=[DataRequired(), Length(min=2, max=20)]
							)
	lastname = StringField('Lastname', 
							validators=[DataRequired(), Length(min=2, max=40)]
							)
	email = StringField('School Email',
						validators=[DataRequired(), Email()]
						)
	password = PasswordField('Password',
							validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',
									validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	# determines if email is unique/already taken
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email is taken. Register with a new one or log in.')


#login form
class LoginForm(FlaskForm):
	email = StringField('Email',
						validators=[DataRequired(), Email()])
	password = PasswordField('Password',
							validators=[DataRequired()])
	remember = BooleanField('Remember Me')
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
