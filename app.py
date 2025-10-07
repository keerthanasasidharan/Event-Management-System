# importing flash modules
from flask import Flask,render_template,flash

# modules for database
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime,date

# for migrating database
from flask_migrate import Migrate

# for hashing
from werkzeug.security import generate_password_hash, check_password_hash

#login
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

#Forms
from webforms import *

#initialising app
app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key"

#initialising database
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:1234@localhost/events'
db = SQLAlchemy(app)
migrate = Migrate(app,db)
ctx = app.app_context()
ctx.push()








class Students(db.Model,UserMixin):
	with app.app_context():
		__table__ = db.Table('students', db.metadata, autoload_with=db.engine)
	def __repr__(self):
		return '<User ID : %r>' %self.student_id

class Clubs(db.Model):
	with app.app_context():
		__table__ = db.Table('clubs', db.metadata, autoload_with=db.engine)
	def __repr__(self):
		return '<Club ID : %r>' %self.club_id

class Events(db.Model):
	with app.app_context():
		__table__ = db.Table('events', db.metadata, autoload_with=db.engine)
	def __repr__(self):
		return '<Event ID : %r>' %self.event_id

class Feedback(db.Model):
	with app.app_context():
		__table__ = db.Table('feedback', db.metadata, autoload_with=db.engine)
	def __repr__(self):
		return '<Feedback ID : %r>' %self.feedback_id

class Notifications(db.Model):
	with app.app_context():
		__table__ = db.Table('notifications', db.metadata, autoload_with=db.engine)
	def __repr__(self):
		return '<Notification ID : %r>' %self.nofit_id

class Participants(db.Model):
	with app.app_context():
		__table__ = db.Table('participants', db.metadata, autoload_with=db.engine)
	def __repr__(self):
		return '<Participants ID : %r>' %self.reg_id

class Venues(db.Model):
	with app.app_context():
		__table__ = db.Table('venues', db.metadata, autoload_with=db.engine)
	def __repr__(self):
		return '<Venue ID : %r>' %self.venue_id

class Venueschedule(db.Model):
	with app.app_context():
		__table__ = db.Table('venueschedule', db.metadata, autoload_with=db.engine)
	def __repr__(self):
		return '<Schedule ID : %r>' %self.schedule_id






# app routes

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/club')
def club():
	return render_template('club.html')

@app.route('/admin')
def admin():
	return render_template('admin.html')

@app.route('/login',methods=['GET','POST'])
def login():
	return render_template('login.html')



@app.route('/register',methods=['GET','POST'])
def register():
	form=StudentForm()
	cform=ClubForm()
	if form.validate_on_submit():
		user= Students.query.filter_by(email=form.email.data).first()
		if user is None:
			hashed_pw = generate_password_hash(form.password1.data)
			student = Students(student_name=form.name.data,
				username=form.username.data,
				email=form.email.data,
				password_hash=hashed_pw,
				department=form.dept.data,
				phone=form.phone.data)
			db.session.add(student)
			db.session.commit()
		else:
			flash("Username already taken")
	elif cform.validate_on_submit():
		club= Clubs.query.filter_by(email=cform.email.data).first()
		if club is None:
			hashed_pw = generate_password_hash(cform.password1.data)
			club = Clubs(club_name=cform.name.data,
				username=cform.username.data,
				email=cform.email.data,
				password_hash=hashed_pw,
				phone=cform.phone.data,
				chairperson=cform.chair.data,
				vice_chairperson=cform.vice.data,
				point_of_contact=cform.poc.data)
			db.session.add(club)
			db.session.commit()
		else:
			flash("Username already taken")
	form.name.data=''
	form.username.data=''
	form.email.data=''
	form.password1.data=''
	form.password2.data=''
	form.dept.data=''
	form.phone.data=''
	cform.name.data=''
	cform.username.data=''
	cform.email.data=''
	cform.password1.data=''
	cform.password2.data=''
	cform.phone.data=''
	cform.chair.data=''
	cform.vice.data=''
	cform.poc.data=''
	return render_template('register.html',form=form,cform=cform)