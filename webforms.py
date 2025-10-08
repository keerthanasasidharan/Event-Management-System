
#for doing forms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, RadioField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo,Length

class StudentForm(FlaskForm):
	role=StringField("Role",default='student')
	name=StringField("Full name", validators=[DataRequired()])
	username=StringField("Username", validators=[DataRequired()])
	email=StringField("Email", validators=[DataRequired()])
	phone=StringField("Phone Number", validators=[DataRequired()])
	dept=SelectField("Department",choices=[('ae',"AE"),('ce','CE'),('cs','CS'),('ec',"EC"),('ee','EE'),('me','ME')],validators=[DataRequired()])
	password1=PasswordField("Password", validators=[DataRequired(),EqualTo('password2',message='Passwords must match')])
	password2=PasswordField("Confirm Password", validators=[DataRequired()])
	submit=SubmitField("Submit")


class ClubForm(FlaskForm):
	role=StringField("Role",default='club')
	name=StringField("Club name", validators=[DataRequired()])
	username=StringField("Username for club account", validators=[DataRequired()])
	email=StringField("Email", validators=[DataRequired()])
	phone=StringField("Phone Number", validators=[DataRequired()])
	chair=StringField("Chairperson", validators=[DataRequired()])
	vice=StringField("Vice Chairperson", validators=[DataRequired()])
	poc=StringField("Point of Contact", validators=[DataRequired()])
	password1=PasswordField("Password", validators=[DataRequired(),EqualTo('password2',message='Passwords must match')])
	password2=PasswordField("Confirm Password", validators=[DataRequired()])
	submit=SubmitField("Submit")

class LoginForm(FlaskForm):
	#role=RadioField("Role",choices=[('student',"Student"),('club',"Club")],default='student')
	username=StringField("Username",validators=[DataRequired()])
	password=PasswordField("Password",validators=[DataRequired()])
	submit=SubmitField("Submit")