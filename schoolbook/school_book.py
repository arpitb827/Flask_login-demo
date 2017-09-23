from flask import Flask, render_template, request, flash,redirect, url_for, session
from forms import LoginForm, RegisterForm,PasswordResetForm,DashBoardForm,Student_Teacher_Form
from flask_sqlalchemy import SQLAlchemy
import datetime

#adding password security using werkzug
from werkzeug.security import generate_password_hash, check_password_hash

#adding flask login to resrict user to do first sign in 
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

#addin oauth for google sign 

from flask_oauth import OAuth

app = Flask(__name__, template_folder='templates')

app.config["SECRET_KEY"]="Thisisascretkey"
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://localhost/schoolbook'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
# Bootstrap(app)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

class Teacher(db.Model):

	__tablename__= 'teacher'

	id = db.Column('id', db.Integer, db.Sequence('teacher_id_seq',start=1), primary_key=True,)
	name = db.Column(db.String(80))
	age = db.Column(db.Integer)
	gender = db.Column(db.String(1))
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Student(db.Model):

	__tablename__= 'student'

	id = db.Column('id', db.Integer, db.Sequence('student_id_seq',start=1), primary_key=True,)
	name = db.Column(db.String(80))
	age = db.Column(db.Integer)
	gender = db.Column(db.String(1))
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class User(UserMixin,db.Model):

	__tablename__ = 'users'
	
	id = db.Column('id', db.Integer, db.Sequence('user_id_seq',start=1), primary_key=True,)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80))
	email = db.Column(db.String(80), unique=True)
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

@app.route("/", methods=["GET","POST"])
@login_required
def home():
	form = DashBoardForm()
	data = []
	# if form.validate_on_submit():
	# 	print "form=========dash==",form.dash_type.data
	# 	if form.dash_type.data=='student':
	# 		data = Student.query.all()
	# 		# return redirect(url_for('get_data'))
	# 	else:
	# 		data = Teacher.query.all()
	# else:
	data = Student.query.all() or Teacher.query.all() 
	return render_template("home.html", name=current_user.username,form=form, datas=data)

@app.route("/login", methods=["GET","POST"])
def signin():
	form = LoginForm()
	if form.validate_on_submit():
		# return '<h1>'+form.username.data +' ' +form.password.data+ '</h1>'
		user = User.query.filter_by(username=form.username.data).first()
		try:
			if user:
				if check_password_hash(user.password,form.password.data) :
					login_user(user, remember=form.remember.data)
					return redirect(url_for('home'))
				else:
					flash("Password does not match.Forgot password ?")

		except Exception as e:
			flash("User does not exist ! Please signup first.")
 
	return render_template("index.html",form=form)


@app.route("/signup", methods=["GET","POST"])
def signup():
	form = RegisterForm()
	if form.validate_on_submit():
		hash_password = generate_password_hash(form.password.data,method='sha256')
		try :
			new_user = User(username=form.username.data, email=form.email.data, password= hash_password)
			db.session.add(new_user)
			db.session.commit()
			flash("User created sucessfully! now login.")
		except Exception as inst:
			flash("Email is already created!.")


		# return "New User Has been created!"
		# return '<h1>'+form.username.data +' ' +form.password.data+ '</h1>'

	return render_template("signup.html", form=form)

@app.route("/logout")
@login_required
def log_out():
	logout_user()
	return redirect(url_for('signin'))

@app.route("/password_reset", methods=["GET","POST"])
def reset_password():
	form = PasswordResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		try:
			if user:
				#when both password are same
				if form.new_password.data == form.confirm_password.data:
					hash_password = generate_password_hash(form.confirm_password.data,method='sha256')
					user.password = hash_password
					db.session.commit()
					flash("Password reset sucessfully!.")
					# return '<h1>'+ 'Password is reset' +'</h1>'
				else:
					flash("Password not match!.")
		except Exception as e:
			flash("There is no user for this Email.")
		

	return render_template("password_reset.html",form=form)

@app.route("/add", methods=["GET","POST"])
def add():
	form = Student_Teacher_Form()
	if form.validate_on_submit():
		if form.type.data=='student':
			student =Student(name=form.name.data, age=int (form.age.data), gender= form.gender.data)
			db.session.add(student)
			db.session.commit()
			flash("Student Created sucessfully!")
		else:
			teacher =Teacher(name=form.name.data, age=int (form.age.data), gender= form.gender.data )
			db.session.add(teacher)
			db.session.commit()
			flash("Teacher Created sucessfully!")
		return redirect(url_for('home'))

	return render_template("add_student.html", form=form)

@app.route("/get_data", methods=["GET","POST"])
def get_data ():
	form = DashBoardForm()
	if form.validate_on_submit():
		if form.dash_type.data=='student':
			data = Student.query.all()
			# return redirect(url_for('get_data'))
		else:
			data = Teacher.query.all()
	return render_template("home.html", name=current_user.username,form=form, datas=data)



if __name__ == '__main__':
   db.create_all()
   app.run(debug=True)
