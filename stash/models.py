from datetime import datetime

from stash.core import db
from stash import app
from stash.core import Security, SQLAlchemyUserDatastore, \
	UserMixin, RoleMixin, login_required, encrypt_password, verify_password


# ----------- User -------------

roles_users = db.Table('roles_users',
	db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
	db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class User(db.Model):
	__tablename__ = 'user'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, unique=True)
	email = db.Column(db.String, unique=True)
	password = db.Column(db.String(255))
	active = db.Column(db.Boolean())
	confirmed_at = db.Column(db.DateTime())
	roles = db.relationship('Role', secondary=roles_users,
		backref=db.backref('users', lazy='dynamic'))

	# Custom methods to manage password auth

	# def hash_password(self, plaintext):
	# 	self.password = encrypt_password(plaintext)

	# def check_password(self, challenge):
		# print 'checking password'
		# return verify_password(challenge, self.password)

	# Methods for login
	
	def is_authenticated(self):
		return True

	def is_active(self):
		return self.active

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % self.username

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

# User security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

def validate_user_request(form):
	return "username" in form and "email" in form and "password" in form

# --------- Tags and Images ------------

tag_image_join_table = db.Table("tags_images", 
	db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
	db.Column('image_id', db.Integer, db.ForeignKey('image.id'))
)

class Image(db.Model):
	__tablename__ = 'image'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	# maybe stupid assumption to make - max url len should be 1024
	url = db.Column(db.String(length=500))  
	created_date = db.Column(db.DateTime)
	# MongoDB ObjectID field encoded as String
	metadata_id = db.Column(db.String(24))  
	tags = db.relationship("Tag", 
		secondary=tag_image_join_table,
		backref=db.backref('images', lazy='dynamic')
	)

	def __init__(self, name, url, created_date=None):
		self.name = name
		self.url = url
		if not created_date:
			created_date = datetime.utcnow()
		self.created_date = created_date
		self.metadata_id = ""

	def __repr__(self):
		return '<Image %r>' % self.url

class Tag(db.Model):
	__tablename__ = 'tag'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Tab %r> ' % self.name

# ----- Not used beyond this point ------

class Post(db.Model):
	__tablename__ = ''
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(length=80))
	body = db.Column(db.Text)
	pub_date = db.Column(db.DateTime)


	def __init__(self, title, body, pub_date=None):
		self.title = title
		self.body = body
		if pub_date is None:
			pub_date = datetime.utcnow()
		self.pub_date = pub_date

	def __repr__(self):
		return '<Post %r>' % self.title

# models for which we want to create API endpoints
# each mapping consists of (name -> model_config)
# which corresponds to kwarg options to 
# Flask-Restless's "create_api" method. 
# Some of the commonly included ones include:
# 	"model_class" Python class to use as API endpoint
# 	"methods" Allowed HTTP methods (GET/POST/PUT/DELETE)
# 	"exclude_columns" Column names to exclude from DB
app.config['API_MODELS'] = {
	'user': {
		'model_class': User,
		'exclude_columns': ['password']
	},
	'tag': {
		'model_class': Tag,
	},
	'image': {
		'model_class': Image
	}
} 

# models for which we want to create CRUD-style URL endpoints,
# and pass the routing onto our AngularJS application
app.config['CRUD_URL_MODELS'] = {
	'tag': Tag,
	'image': Image
}
