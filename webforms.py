
#for doing forms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField, SelectField, RadioField, BooleanField, ValidationError, DateField, TimeField
from wtforms.validators import DataRequired, EqualTo,Length

#inporting textarea which are bigger than regular text fields
from wtforms.widgets import TextArea

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

class EventForm(FlaskForm):
	title = StringField("Event Title", validators=[DataRequired()])
	desc = StringField("Event Description", validators=[DataRequired()],widget=TextArea())
	category = StringField("Category", validators=[DataRequired()])
	date = DateField("Event Date", format='%Y-%m-%d', validators=[DataRequired()])
	stime = TimeField("Event Start Time", format='%H:%M', validators=[DataRequired()])
	etime = TimeField("Event End Time", format='%H:%M', validators=[DataRequired()])
	#venue = SelectField("Venue",choices=[(None,''),(1,"Dhwani"),(2,"Sargam"),(3,'Gazebo'),(4,'DJ Hall'),(5,'CETAA Hall')],validators=[DataRequired()])
	reglink = StringField("Registration Link (optional)")
	event_id = HiddenField()
	submit = SubmitField("create_event")

class ReqVenForm(FlaskForm):
	venue = SelectField("Venue",choices=[(None,''),(1,"Dhwani"),(2,"Sargam"),(3,'Gazebo'),(4,'DJ Hall'),(5,'CETAA Hall')],validators=[DataRequired()])
	date = DateField("Event Date", format='%Y-%m-%d', validators=[DataRequired()])
	stime = TimeField("Event Start Time", format='%H:%M', validators=[DataRequired()])
	etime = TimeField("Event End Time", format='%H:%M', validators=[DataRequired()])
	submit = SubmitField("edit_event")