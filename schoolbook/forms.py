from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField, BooleanField, PasswordField, SubmitField, RadioField, SelectField
from wtforms.validators import InputRequired, Email, Length
from wtforms.fields.html5 import DateField
import datetime


class LoginForm(FlaskForm):

	username = StringField("UserName",validators=[InputRequired("Please enter user name."), Length(min=4, max=15)])
	password = PasswordField("Password",validators=[InputRequired("Please enter password."),Length(min=8, max=80)])
	remember = BooleanField("Remember me")

class RegisterForm(FlaskForm):

	username = StringField("UserName",validators=[InputRequired("Please enter user name."), Length(min=4, max=15)])
	password = PasswordField("Password",validators=[InputRequired("Please enter password."),Length(min=8, max=80)])
	email = StringField("Email", validators= [InputRequired(message="Invalid Email"),Email("Email format is wrong"), Length(max=80)])

class PasswordResetForm(FlaskForm):

	new_password = PasswordField("New Password",validators=[InputRequired("Please enter new password"), Length(min=8, max=80)])
	confirm_password = PasswordField("Confirm Password",validators=[InputRequired("Please confirm password."),Length(min=8, max=80)])
	email = StringField("Email", validators= [InputRequired(message="Invalid Email"),Email("Email format is wrong"), Length(max=80)])

class DashBoardForm(FlaskForm):

	dash_type = SelectField('Select', choices=[('student', 'Student'), 
								('teacher', 'Teacher')], default='student')

	submit = SubmitField("Find Data")

class Student_Teacher_Form(FlaskForm):

	name = StringField("Name", validators=[InputRequired("Please enter Name")])
	age = IntegerField("Age", validators=[InputRequired("Please enter Age")])
	gender = SelectField("Gender", choices=[('M','Male'),('F','Female')])
	type = SelectField("Type", choices=[('student','Student'),('teacher','Teacher')] )
	submit = SubmitField("Save")
