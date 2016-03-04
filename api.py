from flask import (Flask, g, render_template, flash, redirect, url_for, request, abort,jsonify)
from flask.ext.bootstrap import Bootstrap
from flask.ext.bcrypt import check_password_hash # to check the hash of the password
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user #An appliance to handle user authentication. 
import datetime as dt
from functools import wraps
import peewee as pw
from marshmallow import Schema, fields


### API Helpers###
def check_auth(email, password):
    """Check if a username/password combination is valid.
    """
    print email
    print password
    try:
        user = models.User.get(models.User.email == email)
    except models.DoesNotExist:
        return False
    return check_password_hash(user.password,password)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            resp = jsonify({"message": "Please authenticate."})
            resp.status_code = 401
            resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'
            return resp
        return f(*args, **kwargs)
    return decorated


class UserSchema(Schema):
	 #contents=fields.Str()
	 class Meta:
	 	fields=('username','password', 'email','department','joined_at','is_admin')

class PostSchema(Schema):
	#user=fields.Nested(UserSchema)
	class Meta:
		fields=('timestamp', 'content','tag','score','upvote','downvote')
		