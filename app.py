# importing flash modules
from flask import Flask,render_template,flash,redirect,url_for,render_template_string

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

#login stuff - they initiate the login process
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
	user = Usernames.query.filter_by(username=user_id).first()
	if not user:
		return Students.query.get(user_id)
	else:
		type= user.type
	if type=='student':
		return Students.query.get(user_id)
	else:
		return Clubs.query.get(user_id)


class Usernames(db.Model,UserMixin):
	with app.app_context():
		__table__ = db.Table('usernames', db.metadata, autoload_with=db.engine)
	def __repr__(self):
		return '<Username : %r>' %self.username
	def get_id(self):
		return self.username


class Students(db.Model,UserMixin):
	with app.app_context():
		__table__ = db.Table('students', db.metadata, autoload_with=db.engine)
	def __repr__(self):
		return '<User ID : %r>' %self.student_id
	def get_id(self):
		return self.username

class Clubs(db.Model,UserMixin):
	with app.app_context():
		__table__ = db.Table('clubs', db.metadata, autoload_with=db.engine)
	def __repr__(self):
		return '<Club ID : %r>' %self.club_id
	def get_id(self):
		return self.username

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

@app.route('/club',methods=['GET','POST'])
@login_required
def club():
	return render_template('club.html')

@app.route('/admin',methods=['GET','POST'])
@login_required
def admin():
	return render_template('admin.html')

@app.route('/login',methods=['GET','POST'])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		role = Usernames.query.filter_by(username=form.username.data).first()
		if role:
			if role.type=='student':
				student = Students.query.filter_by(username=form.username.data).first()
				if check_password_hash(student.password_hash,form.password.data):
					login_user(student)
					flash("Login successful")
					return render_template('index.html')
				else:
					flash("Wrong password... Try again...")
			elif role.type=='club':
				club = Clubs.query.filter_by(username=form.username.data).first()
				if check_password_hash(club.password_hash,form.password.data):
					login_user(club)
					flash("Login successful")
					return render_template('club.html')
				else:
					flash("Wrong password... Try again...")
			else:
				if form.password.data=='aana':
					login_user(role)
					return render_template('admin.html')
				else:
					# oru security iku vendi
					flash("Username doesn't exist")
		else:
			flash("Username doesn't exist")
	return render_template('login.html',form=form)



@app.route('/register',methods=['GET','POST'])
def register():
	form=StudentForm()
	cform=ClubForm()
	if form.validate_on_submit():
		student= Students.query.filter_by(email=form.email.data).first()
		user = Usernames.query.filter_by(username=form.username.data).first()
		if student is None and user is None:
			hashed_pw = generate_password_hash(form.password1.data)
			student = Students(student_name=form.name.data,
				username=form.username.data,
				email=form.email.data,
				password_hash=hashed_pw,
				department=form.dept.data,
				phone=form.phone.data)
			user = Usernames(username=form.username.data,type='student')
			db.session.add(user)
			db.session.commit()
			db.session.add(student)
			db.session.commit()
			flash("Student registered successfully")
		else:
			flash("Username already taken")
			return render_template('register.html',form=form,cform=cform)
		return render_template('login.html')
	elif cform.validate_on_submit():
		club= Clubs.query.filter_by(email=cform.email.data).first()
		user = Usernames.query.filter_by(username=cform.username.data).first()
		if club is None and user is None:
			hashed_pw = generate_password_hash(cform.password1.data)
			club = Clubs(club_name=cform.name.data,
				username=cform.username.data,
				email=cform.email.data,
				password_hash=hashed_pw,
				phone=cform.phone.data,
				chairperson=cform.chair.data,
				vice_chairperson=cform.vice.data,
				point_of_contact=cform.poc.data)
			user = Usernames(username=cform.username.data,type='club')
			db.session.add(user)
			db.session.commit()
			db.session.add(club)
			db.session.commit()
			flash("Club registered successfully")
		else:
			flash("Username already taken")
			return render_template('register.html',form=form,cform=cform)
		return render_template('login.html')
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