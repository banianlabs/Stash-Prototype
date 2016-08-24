import os

from flask import Flask, request, Response
from flask import render_template, url_for, redirect, send_from_directory, flash
from flask import send_file, make_response, abort

from flask.ext.login import logout_user
from flask.ext.security.core import current_user
from flask.ext.security.decorators import login_required

from stash import app

# routing for API endpoints (generated from the models designated as API_MODELS)
from stash.core import api_manager
from stash.models import *

default_model_config = {
	'url_prefix': app.config['API_ENDPOINT_PREFIX'],
	'methods': ['GET', 'POST']
} 

for model_name in app.config['API_MODELS']:
	model_config = default_model_config.copy()
	model_config.update(app.config['API_MODELS'][model_name])
	model_class = model_config.pop('model_class')
	api_manager.create_api(model_class, **model_config)

session = api_manager.session

# -------- User ----------

# @app.route('/register', methods=['GET', 'POST'])
# def register():
# 	if request.method == 'GET':
# 		return render_template('register.html')

# 	if not validate_user_registration(request.form):
# 		flash('You need more info')
# 		return redirect('/register')

# 	user = User(username=request.form['username'],
# 		password=request.form['password'],
# 		email=request.form['email'])

# 	db.session.add(user)
# 	db.session.commit()
# 	flash('User successfully logged in')
# 	return redirect("/login")

# @app.route('/login', methods=['GET', 'POST'])
# def login():
# 	print 'here in login'
# 	if request.method == 'GET':
# 		return render_template('login.html')

# 	if not validate_user_login(request.form):
# 		flash('Not enough credentials')
# 		return redirect('/login')

# 	username = request.form['username']
# 	password = request.form['password']
# 	registered_user = User.query.filter_by(username=username)
# 	if registered_user != None and registered_user.check_password(password):
# 		flash('Username or password is invalid', 'error')
# 	login_user(registered_user)
# 	flash('Logged in successfully')
# 	return redirect(request.args.get('next') or "/")	

@app.route('/logout')
def logout():
	logout_user()
	return redirect_url("/")

# -------- API -------------

# routing for basic pages (pass routing onto the Angular app)
@app.route('/')
@app.route('/about')
@app.route('/blog')
def basic_pages(**kwargs):
	return make_response(open('stash/templates/index.html').read())

# routing for CRUD-style endpoints
# passes routing onto the angular frontend if the requested resource exists
from sqlalchemy.sql import exists

crud_url_models = app.config['CRUD_URL_MODELS']

@app.route('/<model_name>/')
@app.route('/<model_name>/<item_id>')
def rest_pages(model_name, item_id=None):
	if model_name in crud_url_models:
		model_class = crud_url_models[model_name]
		if item_id is None or session.query(exists().where(
			model_class.id == item_id)).scalar():
			return make_response(open(
				'stash/templates/index.html').read())
	abort(404)

# gets current user data as json
@app.route('/me/')
def who_am_i():
	if hasattr(g, 'user'):
		return make_response(
			json.dumps({
				'username': g.current_user.username,
				'email': g.current_user.email,
				'confirmed_at': g.current_user.confirmed_at
			})
		)
	else:
		abort(404)

# special file handlers and error handlers
@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
							   'img/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404