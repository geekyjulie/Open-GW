import datetime

from flask.ext.login import UserMixin
from flask.ext.bcrypt import generate_password_hash, check_password_hash
from peewee import *

from marshmallow import Schema, fields
# we can connect it to any other database 
DATABASE = SqliteDatabase('openGW.db')

class BaseModel(Model):
	def __marshallable__(self):
		return dict(self.__dict__)['_data']
	class Meta:
		database=DATABASE

# user model The also include the CRUD operations
class User(UserMixin, Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField(max_length= 100)
	name =  CharField()
	department =  CharField()
	joined_at = DateTimeField(default=datetime.datetime.now)
	is_admin = BooleanField(default=True)


	class Meta:
		database = DATABASE
		order_by = ('-joined_at',)


	# User READ methods
	def get_posts(self): # READ posts made by user 
		return Post.select().where(Post.user == self)

	def get_stream(self): # function to get posts of user and his/her followers
		return Post.select().where(
			(Post.user << self.get_following()) |
			(Post.user == self)
			)

	def get_comments(self): # READ user comments
		pass 

	def get_user(Userid): # READ single User
		return self.select().where(User.id == Userid).get()

	def get_following(self):
		""" the users we are following """
		return (User.select().join(
				Relationship, on=Relationship.to_user).where(
				Relationship.from_user == self
				))

	def get_followers(self):
		""" the users who are following the current user"""
		return (User.select().join(
				Relationship, on=Relationship.from_user).where(
				Relationship.to_user == self
				))



	# User UPDATE methods
	def update_username(username):
		pass

	def update_email(email):
		pass

	def update_password(password):
		pass

	def update_name(name):
		pass

	def update_department(department):
		pass


	# DELETE User
	def delete_user(userId):
		pass


	# User CREATE method 
	@classmethod
	def create_user(cls, username, email, password, name, department, is_admin=False): # CREATE user 
		try:
			with DATABASE.transaction():
				cls.create(
					username = username,
					email = email, 
					password = generate_password_hash(password), # encripting the password for security 
					name = name,
					department = department)

		except IntegrityError: raise ValueError("User already exists")






# Relationship Model (user following)
class Relationship(Model):
	from_user = ForeignKeyField(
		rel_model=User, # what class does it relate too
		related_name='relationships' #this is what the related model would call this model
		)
	to_user = ForeignKeyField(
		rel_model=User, # what class does it relate too
		related_name='related_to' #this is what the related model would call this model
		)

	class Meta:
		database = DATABASE
		indexes =(
				(('from_user', 'to_user'), True)
			)





# our post model
class Post(Model):
	timestamp = DateTimeField(default=datetime.datetime.now)
	user = ForeignKeyField(
		rel_model=User, # what class does it relate too
		related_name='posts' #this is what the related model would call this model
		)
	content = TextField()
	tag = CharField()
	upvote = IntegerField()
	downvote = IntegerField()
	score = IntegerField()


	class Meta:
		database = DATABASE
		order_by = ('-score',) # ordered by score

	# READ operations
	def get_comments(self): #add code to get post comments
		return Comment.select().where(Comment.post == self)

	def get_post(postid):
		return Post.select().where(Post.id == postid)

	def get_user_post(username):
		return Post.select().where(Post.user.username == username)


	# UPDATE Operations
	def edit_post(content, post):
		""" Edits the post content """
		return Post.update(content=content).where(Post.post.id == self.id)

	


# our comment model
class Comment(Model):
	timestamp = DateTimeField(default=datetime.datetime.now)
	content = TextField()
	user = ForeignKeyField(
		rel_model=User, # what class does it relate too
		related_name='user_comments' #this is what the related model would call this model
		)
	post = ForeignKeyField(
		rel_model=Post, # what class does it relate too
		related_name='post_comments' #this is what the related model would call this model
		)
	upvote = IntegerField(default=0)
	downvote = IntegerField(default=0)
	score = IntegerField(default=0)


	class Meta:
		database = DATABASE
		order_by = ('-timestamp',) # temperarly I am ordering them by the time they're poster 
		# we need to fix it to be ordered by score




def initialize(): # to initialize our model
	DATABASE.connect()
	DATABASE.create_tables([User, Post, Comment, Relationship], safe=True)
	DATABASE.close()
