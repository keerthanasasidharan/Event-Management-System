# importing flash modules
from flask import Flask,render_template,request,flash,redirect,url_for,render_template_string

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

#for date and time
from datetime import datetime

#Forms
from webforms import *

#initialising app
app = Flask(__name__)
app.secret_key = 'some_very_secret_key'

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
login_manager.session_protection = "strong"
@login_manager.user_loader
def load_user(user_id):
	user = Usernames.query.filter_by(username=user_id).first()
	if not user:
		return None
	if user.type == 'student':
		return Students.query.filter_by(username=user_id).first()
	elif user.type == 'club':
		return Clubs.query.filter_by(username=user_id).first()
	elif user.type == 'admin':
		return user
	return None


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
@app.route('/', methods=['GET', 'POST'])
def index():
	form = StudentForm()
	
	if current_user.is_authenticated and current_user.type=='students':
		student = Students.query.filter_by(username=current_user.username).first()
		if not student:
			flash("Error updating profile. Try again.")
		elif 'reg_event' not in request.form and request.method == 'POST':
			student.student_name = request.form['name']
			student.username = request.form['username']
			student.department = request.form['dept']
			student.phone = request.form['phone']
			student.email = request.form['email']

			try:
				db.session.commit()
				flash("Updated successfully")
			except:
				flash("Error updating profile. Try again.")
		elif 'reg_event' in request.form and request.method == 'POST':
			try:
				print(request.form.get('event_id'),request.form.get('student_id'))
				result = db.session.execute(text("CALL REGISTERFOREVENT(:event_id, :student_id)"),
					{
						'event_id': request.form.get('event_id'),
						'student_id': request.form.get('student_id')
					}
				)
				db.session.commit()
				message_row = result.fetchone()
				if message_row:
					flash(message_row[0])  # the 'message' column as returned from the procedure
				else:
					flash("No message returned from procedure")
				return redirect(url_for('index'))
			except Exception as e:
				db.session.rollback()
				print({'error':str(e)})
	elif not current_user.is_authenticated or current_user.type=='clubs':
		flash("You must login to register or volunteer in events")
	events = Events.query.order_by(Events.event_date.desc())
	clubs = Clubs.query.with_entities(Clubs.club_id,Clubs.club_name).all()
	venues = Venues.query.with_entities(Venues.venue_id,Venues.venue_name).all()
	club_lookup = {club.club_id: club.club_name for club in clubs}
	venue_lookup = {venue.venue_id: venue.venue_name for venue in venues}
	venueschedule = db.session.query(Venueschedule).all()
	schedule_lookup = {s.event_id: s.venue_id for s in venueschedule}
	participants = db.session.query(Participants).all()
	p_lookup = {(p.student_id,p.event_id): p.participant_id for p in participants}
	return render_template('index.html', form=form,events=events,club_lookup=club_lookup,venue_lookup=venue_lookup,schedule_lookup=schedule_lookup,p_lookup=p_lookup,now=date.today())




@app.route('/club',methods=['GET','POST'])
@login_required
def club():
	form = ClubForm()
	eform = EventForm()
	vform = ReqVenForm()
	if current_user.type=='students':
		flash("Unauthorized access!!")
		return redirect(url_for('index'))
	elif 'edit_profile' in request.form:
		club = Clubs.query.filter_by(username=current_user.username).first()
		if not club:
			flash("Error updating profile. Try again.")
		elif request.method == 'POST':
			club.club_name = request.form['name']
			club.username = request.form['username']
			club.chairperson = request.form['chair']
			club.vice_chairperson = request.form['vice']
			club.point_of_contact = request.form['poc']
			club.phone = request.form['phone']
			club.email = request.form['email']

			try:
				db.session.commit()
				flash("Updated successfully")
				return redirect(url_for('club'))
			except:
				flash("Error updating profile. Try again.")
	elif 'create_event' in request.form:
		if request.method == 'POST':
			try:
				result = db.session.execute(text("CALL CreateEvent(:club_id, :title, :description, :category, :event_date, :event_time, :event_endtime,:reg_last_date, :reg_link)"),
					{
						'club_id': current_user.club_id,
						'title': eform.title.data,
						'description': eform.desc.data,
						'category': eform.category.data,
						'event_date': None,
						'event_time': None,
						'event_endtime' : None,
						'reg_last_date': None,
						'reg_link': eform.reglink.data
					}
				)
				db.session.commit()

				flash("Event created successfully")
				return redirect(url_for('club'))
			except Exception as e:
				db.session.rollback()
				print({'error':str(e)})
	elif 'edit_event' in request.form:
		if request.method == 'POST':
			print(request.form)
			event_id = request.form.get('event_id')
			event= Events.query.get(event_id)
			try:
				event.title=eform.title.data
				event.desc=eform.desc.data
				event.category=eform.category.data
				event.reg_link=eform.reglink.data
				db.session.commit()
				flash("Event edited successfully")
				return redirect(url_for('club'))
			except Exception as e:
				print(event_id)
				db.session.rollback()
				print({'error':str(e)})
	elif 'req_event' in request.form:
		if request.method == 'POST':
			try:
				result = db.session.execute(text("CALL REQUESTVENUE(:event_id, :venue_id, :start, :end)"),
					{
						'event_id': request.form.get('event_id'),
						'venue_id': vform.venue.data,
						'start': str(vform.date.data)+' '+str(vform.stime.data),
						'end': str(vform.date.data)+' '+str(vform.etime.data)
					}
				)
				db.session.commit()
				message_row = result.fetchone()
				if message_row:
					flash(message_row[0])  # the 'message' column as returned from the procedure
				else:
					flash("No message returned from procedure")
				return redirect(url_for('club'))
			except Exception as e:
				db.session.rollback()
				print({'error':str(e)})
	events = Events.query.filter_by(club_id=current_user.club_id).order_by(Events.event_date)
	venueschedule = db.session.query(Venueschedule).all()
	schedule_lookup = {s.event_id: s.venue_id for s in venueschedule}
	venues = Venues.query.with_entities(Venues.venue_id,Venues.venue_name).all()
	venue_lookup = {venue.venue_id: venue.venue_name for venue in venues}
	return render_template('club.html', form=form,eform=eform,vform=vform,events=events,schedule_lookup=schedule_lookup,venue_lookup=venue_lookup,now=date.today())


@app.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		flash("You have already signed in")
		return redirect(url_for('index' if current_user.type=='students' else 'club'))
	form=LoginForm()
	if form.validate_on_submit():
		role = Usernames.query.filter_by(username=form.username.data).first()
		if role:
			if role.type=='student':
				student = Students.query.filter_by(username=form.username.data).first()
				if check_password_hash(student.password_hash,form.password.data):
					login_user(student,remember=True)
					print("Logged in user:", current_user.username)
					print("Is authenticated:", current_user.is_authenticated)
					flash("Login successful")
					return redirect(url_for('index'))
				else:
					flash("Wrong password... Try again...")
			elif role.type=='club':
				club = Clubs.query.filter_by(username=form.username.data).first()
				if check_password_hash(club.password_hash,form.password.data):
					login_user(club,remember=True)
					flash("Login successful")
					return redirect(url_for('club'))
				else:
					flash("Wrong password... Try again...")
		else:
			flash("Username doesn't exist")
	return render_template('login.html',form=form)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash("You have been logged out.")
	return redirect(url_for('login'))



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
			return redirect(url_for('login'))
		elif student is None:
			flash("Username already taken")
		else:
			flash("Email already in use")
			return render_template('register.html',form=form,cform=cform)
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
			return redirect(url_for('login'))
		elif student is None:
			flash("Username already taken")
		else:
			flash("Email already in use")
			return render_template('register.html',form=form,cform=cform)
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

