# definition of all forms in application 

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, SelectMultipleField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from bronco_buddies.models import User, Forum

def forum_query():
    return Forum.query


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
	submit = SubmitField('Log In')


class NewPostForm(FlaskForm):
	title = StringField('Title',
						validators=[DataRequired()])
	content = TextAreaField('Question Body',render_kw={"rows": 5, "cols": 11},
						validators=[DataRequired()])

	# replace current choices with a query for all rows in forum table 
	# forumType = SelectField('Question Type',
	# 					validators=[DataRequired()],
	# 					choices=[('1','Student Life on Campus'), ('2','Technology'), ('3','Random'), ('4','Homework')])
	forumType = QuerySelectField('Question Type', validators=[DataRequired()], query_factory=forum_query, allow_blank=True, get_label="title")
	submit = SubmitField('Post')


class NewForumForm(FlaskForm):
	title = StringField('Title',
						validators=[DataRequired()])
	description = StringField('Forum Description', render_kw={"rows": 5, "cols": 11})
	submit = SubmitField('Create Forum')

class ReplyForm(FlaskForm):
	body = TextAreaField('Your Response',render_kw={"rows": 5, "cols": 11},
						validators=[DataRequired()])
	submit = SubmitField('Post')
