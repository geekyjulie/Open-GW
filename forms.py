# this script is for form validation we use the flask extention wtforms to validate a user 
# all the imported libraries are functions that help in validation
from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, Length, EqualTo

from models import User # we import our user model



def name_exists(form, field): # a custom function to check if the username already exists in the database
	if User.select().where(User.username == field.data).exists():
		raise ValidationError('User with that username already exitst.') # if it does exist it throws a validation error

def email_exists(form, field): # a custom function to check if the email already exists in the database
	if User.select().where(User.email == field.data).exists():
		raise ValidationError('User with that email already exitst.') # if it does exist it throws a validation error




# our registration class for our view template form
class RegisterForm(Form):
	# these are the fields in our form th evalidators are what is expected for the data to have
	# such as must have data, its format, it's length and so on
	username = StringField('Username', 
		validators=[DataRequired(), 
		Regexp(r'^[a-zA-Z0-9_]+$', message='Username should be letters, numbers, underscore, and at least one word.'), 
		name_exists])

	email = StringField('Email', 
		validators=[DataRequired(), 
		Email(),
		email_exists])
	
	password = PasswordField('Password', 
		validators=[DataRequired(), 
		Length(min=6),
		EqualTo('password2', message='Passwords must match.')])

	password2 = PasswordField('Confirm Password', 
		validators=[DataRequired()])

	name = StringField('Name', 
		validators=[DataRequired(), 
		Regexp(r'^[a-zA-Z ]+$', message='Name should be letters, and at least one word.')])

	department = StringField('Department', 
		validators=[DataRequired()])


class EditProfileForm(Form):
	# these are the fields in our form th evalidators are what is expected for the data to have
	# such as must have data, its format, it's length and so on
	username = StringField('Username', 
		validators=[DataRequired(), 
		Regexp(r'^[a-zA-Z0-9_]+$', message='Username should be letters, numbers, underscore, and at least one word.')])

	email = StringField('Email', 
		validators=[DataRequired(), 
		Email()])
	
	password = PasswordField('Password', 
		validators=[DataRequired(), 
		Length(min=6),
		EqualTo('password2', message='Passwords must match.')])

	password2 = PasswordField('Confirm Password', 
		validators=[DataRequired()])

	name = StringField('Name', 
		validators=[DataRequired(), 
		Regexp(r'^[a-zA-Z ]+$', message='Name should be letters, and at least one word.')])

	department = StringField('Department', 
		validators=[DataRequired()])

# our login class for the login template
class LoginForm(Form):

	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])



# our post form 
class PostForm(Form):

	# question = StringField('What do you want to ask?', validators=[DataRequired()])
	content = TextAreaField("Question detail", validators=[DataRequired()])
	tag = SelectField(u'Tag', choices=[('General', 'Help'), ('Programming', 'Python'), ('Department', 'Computer Science')])



# our comment form 
class CommentForm(Form):
	content = TextAreaField("Leave a comment", validators=[DataRequired()])




