from flask import Flask, request
from flask import render_template, redirect, url_for, session
import os
import json
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, validators
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField
from flask_mail import Message, Mail


app = Flask(__name__)
app.config['SECRET_KEY'] = "1234"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'survivorCSC214@gmail.com'
app.config['MAIL_PASSWORD'] = 'UofRSurvivor214'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/')
def landing():
	return render_template('Landing.html')

class loginForm(FlaskForm):
	username = StringField('Username:', validators=[DataRequired()])
	password = StringField('Password:', validators=[DataRequired()])
	submit = SubmitField('Submit')

@app.route('/login',  methods=['GET', 'POST'])
def login():
	username = ""
	password = ""
	form = loginForm()
	form.validate()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		# We will need to check here if the user already exists in the data base 
			# if they do exist continue with current code	
			# Otherwise 
				#return redirect(url_for('createaccount'))
		return render_template('Game-Page.html', uname=username)
	return render_template('Login.html', form=form, username=username, password=password)


class accountInfo(FlaskForm):
	fname = StringField('First Name:', validators=[DataRequired()]) 
	lname = StringField('Last Name:', validators=[DataRequired()])
	email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
	username = StringField('Username:', validators=[DataRequired()])
	password = StringField('Password:', validators=[DataRequired()])
	submit = SubmitField('Submit')

@app.route('/createaccount',  methods=['GET', 'POST'])
def createaccount():
	fname = ""
	lname = ""
	email = ""
	username = ""
	password = ""
	form = accountInfo()
	form.validate()
	if form.validate_on_submit():
		fname = form.fname.data
		lname = form.lname.data
		email = form.email.data
		username = form.username.data
		password = form.password.data 
		msg = Message('Hello from the other side!', sender =   'jcstewart1829@gmail.com', recipients = [email])
  		msg.body = "Hey " + fname + ", \n\nWe are glad you have closen to join our Fantasy Surviror Game. This is you username and password incase you forget.\n\n" + username + "\n" + password + "\n\nHave fun!\nSurvivor Team"
  		mail.send(msg)
		# We will need to check here if the user already exists in the data base 
			# if they do exist
				#return redirect(url_for('login'))
			# Otherwise continues with current code
		# This is where password hashing will happen
		return render_template('Game-Page.html', uname=username)
	return render_template('Create-Account.html', form=form, fname=fname , lname=lname , username=username, password=password, email=email)











