from flask import render_template, flash, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from dashapp import application
from dashapp.forms import LoginForm
from dashapp.models import User
from dashapp import demo_app


@application.route('/')
@application.route('/home')
@login_required
def home():
	return render_template('home.html')

@application.route('/login', methods = ['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		session['username'] = current_user.username
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		session['username'] = form.username.data
		user = User.query.filter_by(username = form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember = form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('home')
		return redirect(next_page)
	return render_template('login.html', form = form)

@application.route('/logout')
def logout():
	session.pop('username', None)
	logout_user()
	return redirect(url_for('login'))
