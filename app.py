from flask import (Flask, g, render_template, flash, redirect, url_for, request, abort,jsonify)
from flask.ext.bootstrap import Bootstrap
from flask.ext.bcrypt import check_password_hash # to check the hash of the password
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user #An appliance to handle user authentication. 
import datetime as dt
from functools import wraps
import peewee as pw
from marshmallow import Schema, fields



import models # to get our models
import forms # to get our forms
import api
from ranking_system import score, top_rank


DEBUG = True

app = Flask(__name__) # initializing the Flask application
app.secret_key = 'fgsajnfiuw3wrejioqr/r2cjean[0i9ecsj2qa' # we add a secete key because we'll be using sessions

login_manager = LoginManager() # setting up the login manager for the app
login_manager.init_app(app)
login_manager.login_view = 'login' 

bootstrap = Bootstrap() # setting up the bootstrap template
bootstrap.init_app(app)

### API Helpers###


### API stuff ###
@app.route('/api/allusers')
@api.requires_auth
def getuser():
	query=models.User.select()
	serializer=UserSchema(many=True)
	result=serializer.dump(query)

	return jsonify({"users": result.data})

@app.route('/api/users')
@api.requires_auth
def getalluser():
	query=models.User.select().where(models.User.email==request.authorization.username)
	serializer=api.UserSchema(many=True)
	result=serializer.dump(query)

	return jsonify({"users": result.data})

#Get all posts
@app.route('/api/posts')
def getallpost():
	query=models.Post.select()
	serializer=api.PostSchema(many=True)
	result=serializer.dump(query)
	return jsonify({"posts":result.data})

#Get a single post
@app.route('/api/posts/<postid>')
def getsinglepost(postid=None):
	query=models.Post.select().where(models.Post.id==postid)
	serializer=api.PostSchema(many=True)
	result=serializer.dump(query)
	return jsonify({"posts":result.data})

@app.route("/api/posts/new", methods=["POST"])
@api.requires_auth
def new_api_post():
    newpost, errs = api.PostSchema().load({
        'content': request.json['content'],
        'user': request.authorization.username,
        'timestamp': dt.datetime.now(),
        'score': 0,
        'upvote':0,
        'downvote':0,
        'tag': request.json['tag']
        
    })
    print newpost
    #newpost.save()
    data, errors = api.PostSchema().dump(newpost)
    if errors:
        return jsonify(errors), 400
    return jsonify({"message": "Successfully created new post item.",
                    "newpost": data})




@login_manager.user_loader # A decorator to mark the function responsible for loading a user from whatever data source we use.
def load_user(userid):
	try:
		return models.User.get(models.User.id == userid) # checking the user if they exits or not 

	except models.DoesNotExist:
		return None


@app.before_request # A decorator to mark a function as running before the request hits a view.
def before_request():
	""" Connect to the database before each request."""
	g.db = models.DATABASE # g - A global object that Flask uses for passing information between views and modules.
	g.db.connect() # connecting to the database
	g.user = current_user


@app.after_request # A decorator to mark a function as running before the response is returned.
def after_request(response):
	""" Close the database connection after each request. """
	g.db.close() # close the database connection
	return response




@app.route('/register', methods=('GET', 'POST'))
def register():
	form = forms.RegisterForm()
	if form.validate_on_submit(): # When the form is submitted through POST, make sure the data is valid.
		flash('You\'ve been registered!', 'alert-success')
		models.User.create_user(username=form.username.data, email=form.email.data, password=form.password.data, name=form.name.data, department=form.department.data) # getting the data out of the form and assigning it to the user model
		return redirect(url_for('index'))
	return render_template('register.html', form=form)



@app.route('/login', methods=('GET', 'POST'))
def login():
	form = forms.LoginForm()
	if form.validate_on_submit():
		try:
			user = models.User.get(models.User.email == form.email.data) # try to get the user from the database
		except models.DoesNotExist:
			flash("Your email or password doesn't match!", 'alert-danger')
		else:
			if check_password_hash(user.password, form.password.data): # check if the password is right
				login_user(user) #login_user - Function to log a user in and set the appropriate cookie so they'll be considered authenticated by Flask-Login
				flash("You've been logged in!", 'alert-success')
				return redirect(url_for('index'))
			else:
				flash("Your email or password doen't match!", 'alert-danger')
	return render_template('login.html', form=form)



@app.route('/logout')
@login_required # Decorator to mark a view as requiring a user to be logged in before they can access the view.
def logout():
	logout_user() # Method to remove a user's session and sign them out.
	flash("You've been logged out! Come back soon.", 'alert-success')
	return redirect(url_for('index'))


# user CRUD
# 
# STILL NEEDS FIXING
# 
@app.route('/account/')
@app.route('/account/<mode>/<usrname>', methods=('GET', 'POST'))
@app.route('/account/<mode>/<usrname>')
@login_required
def account(usrname=None, mode=None):
	user = current_user
	if (usrname and mode=='edit'):
		form = forms.EditProfileForm()
		if form.validate_on_submit(): # When the form is submitted through POST, make sure the data is valid.
 			updated=models.User.update(username=form.username.data, email=form.email.data, password=form.password.data, name=form.name.data, department=form.department.data).where(models.User.username==usrname) # getting the data out of the form and assigning it to the user model
 			updated.execute()
 			flash('Your profile\'ve been updated!', 'alert-success')
 			return redirect(url_for('index'))
		form.username.data=user.username
		form.email.data=user.email
		form.password.data=user.password
		form.name.data=user.name
		form.department.data=user.department
		return render_template('account_edit.html', user=user,form=form)
	elif (usrname and mode=='delete'):
		logout_user()
		deleted=models.User.delete().where(models.User.username==usrname)
		deleted.execute()
		flash('Your profile\'ve been deleted!', 'alert-success')
		return redirect(url_for('index'))
	return render_template('account.html', user=user)

@app.route('/new_post', methods=('GET', 'POST'))
@login_required
def post():
	form = forms.PostForm()
	if form.validate_on_submit():
		models.Post.create(user=g.user._get_current_object(), content=form.content.data.strip(), tag=form.tag.data, upvote=0, downvote=0, score=0)
		flash("Question posted!", 'alert-success')
		return redirect(url_for('index'))
	return render_template('post.html', form=form)



@app.route('/')
def index():
	stream = models.Post.select().limit(100)
	return render_template('stream.html', stream=stream)


@app.route('/stream')
@app.route('/stream/<username>')
def stream(username=None):
    template = 'stream.html'
    if username and username != current_user.username:
    	try:
        	user = models.User.select().where(models.User.username**username).get() # ** compare if match
        except models.DoesNotExist:
        	abort(404)
        else:
        	stream = user.posts.limit(100)

    else: # our username
        stream = current_user.get_stream().limit(100)
        user = current_user

    if username:
        template = 'user_stream.html'
    return render_template(template, stream=stream, user=user)



# updating the upvotes
@app.route('/upvote/', methods=('GET', 'POST'))
@app.route('/upvote/<int:post_id>', methods=('Get', 'Post'))
@login_required
def update_vote(post_id=None):

	postNumber = request.args.get('postid', post_id)
	post = models.Post.select().where(models.Post.id == postNumber).get()
	post.upvote = post.upvote + 1
	update_score = top_rank(post)
	post.score = update_score
	post.save()		
	
	return redirect(url_for('stream'))
		

# updating the downvote
@app.route('/downvote/', methods=('GET', 'POST'))
@app.route('/downvote/<int:post_id>', methods=('Get', 'Post'))
@login_required
def downvote_vote(post_id=None):

	postNumber = request.args.get('postid', post_id)
	post = models.Post.select().where(models.Post.id == postNumber).get()
	post.downvote = post.downvote + 1
	update_score = top_rank(post)
	post.score = update_score
	post.save()		
			
	return redirect(url_for('stream'))
		


# 
# STILL NEEDS FIXING [in comments section]
# 

@app.route('/post/',  methods=('GET', 'POST'))
@app.route('/post/<int:postid>',  methods=('GET', 'POST'))
@login_required
def singlepost(postid=None):
	postNumber = request.args.get('post', postid)
	try:
		post = models.Post.select().where(models.Post.id == postNumber).get()
		comments = models.Comment.select().where(models.Comment.post == post).limit(100)
	except models.DoesNotExist:
		abort(404)
		pass
	else:
		form = forms.CommentForm()
		if form.validate_on_submit():
			models.Comment.create(content=form.content.data.strip(), post=post , user=g.user._get_current_object())
			flash("Comment posted!", 'alert-success')
			return render_template("singlepost.html", post=post, form=form, comments=comments)

	return render_template("singlepost.html", post=post, form=form, comments=comments)




@app.route('/edit/<int:postid>', methods=('GET', 'POST'))
@login_required
def edit_post(postid=None):
	post = models.Post.select().where(models.Post.id == postid).get()

	form = forms.PostForm()
	if form.validate_on_submit():
		post.content = form.content.data.strip()
		post.save()	
		flash("Post edited successfuly!", 'alert-success')
		form2= forms.CommentForm()
		return render_template("singlepost.html", post=post, form=form2)

	return render_template("editpost.html", post=post, form=form)

#todo: delete comments first, pop up from javasrcript - confirm or cancel
@app.route('/delete_post/<int:postid>')
@login_required
def delete_post(postid=None):

	deleted=models.Post.delete().where(models.Post.id==postid)
	deleted.execute()
	flash("Your post has been deleted!", 'alert-success')
	return redirect(url_for('index'))

#todo: alert from javascript - confirm or cancel
@app.route('/edit_comment/<int:commentid>', methods=('GET','POST'))
@login_required
def edit_comment(commentid=None):
	comment = models.Comment.select().where(models.Comment.id == commentid).get()

	form = forms.CommentForm()
	if form.validate_on_submit():
		comment.content = form.content.data.strip()
		comment.save()	
		flash("Comment edited successfuly!", 'alert-success')
		#form2= forms.CommentForm()
		return redirect(url_for('index'))

	return render_template("editcomment.html", post=post, form=form)

@app.route('/delete_comment/<int:commentid>')
@login_required
def delete_comment(commentid=None):

	deleted=models.Comment.delete().where(models.Comment.id==commentid)
	deleted.execute()
	flash("Your comment has been deleted!", 'alert-success')
	return redirect(url_for('index'))

@app.route('/follow/<username>')
@login_required
def follow(username):
	try:
		to_user = models.User.get(models.User.username**username)
	except models.DoesNotExist:
		abort(404)
	else:
		try:
			models.Relationship.create(from_user=g.user._get_current_object(), 
				to_user=to_user)
		except models.IntegrityError:
			pass
		else:
			flash('You are now following {}!'.format(to_user.username), 'alert-success')

	return redirect(url_for('stream', username=to_user.username))



@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
	try:
		to_user = models.User.get(models.User.username**username)
	except models.DoesNotExist:
		abort(404)
	else:
		try:
			models.Relationship.get(from_user=g.user._get_current_object(), 
				to_user=to_user).delete_instance()
		except models.IntegrityError:
			pass
		else:
			flash('You have unfollowing {}!'.format(to_user.username), 'alert-success')

	return redirect(url_for('stream', username=to_user.username))




@app.errorhandler(404) # error handeling view function
def not_found(error):
	return render_template('404.html'), 404



if __name__ == '__main__': # launching our falsk application
	
	models.initialize() # initializing our models in the database 

	try:
		models.User.create_user(username='athoug', email='athoug@gwu.edu', password='password', name='Athoug Alsoughayer', department='CS') # for testing purposes 
	
	except ValueError:
		pass	

	app.run(debug=DEBUG)





