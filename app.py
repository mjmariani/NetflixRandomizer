import os

from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, login_required, logout_user, current_user, login_user, UserMixin, current_user

from forms import *
from models import *

CURR_USER_KEY = 1

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.config['TESTING'] = True
app.testing = True

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/randomizer'))

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/randomizer'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "this really needs to be changed")
app.run(use_reloader=True)
toolbar = DebugToolbarExtension(app)


connect_db(app)
# db.drop_all()
# db.create_all()
########################################################################################################
#User signup/login/logout
##The bottom code for before request, login, logout come from Springboard warbler project code

@app.before_request
def add_user_to_g():
    """adding user to global object. If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
        
    else:
        g.user = None
        
def do_login(user):
    """Log in user."""
    
    session[CURR_USER_KEY] = user.id
    
def do_logout():
    """Logout user."""
    
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        
###I have plans on implementing Flask-Login after submission of capstone 

########################################################################################################
##Information Page

@app.route('/info')
def info():
    """Show info page"""
    
    return render_template('info.html')

@app.route('/users/<int:user_id>')
def details():
    """Show profile details page"""
    
    return render_template('users/details.html')

@app.route('/edit', methods=["GET", "POST"])
def edit():
    """edit user information"""
    
    return render_template('users/edit.html')

@app.route('/friend_detail.html')
def friend_detail():
    
    """freind's details"""
    
    return render_template('/users/friend_detail.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    
    """handle user login"""
    
    return render_template('/users/login.html')

@app.route('/signup', methods=["GET", "POST"])
def sign_up():
    """handle user sign up"""
    
    return render_template('/users/signup.html')

@app.route('/show', methods=["GET", "POST"])
def show():
    
    """To show and run the netflix randomizer"""
    
    return render_template('/users/show.html')



########################################################################################################
#Homepage and error pages

@app.route('/')
def home():
    """Show homepage
    """
    
    return render_template('home.html')

@app.route('/home')
def home_page():
    
    return redirect('/')

########################################################################################################
#Accepting Friend Requests and Deleting Friend requests


@app.route('/add_friend/<int:user_id>', methods=['POST'])
def accept_friend_request():
    """accepting friend's request"""
    
    ##Used the following code for help in setting this code: https://github.com/logicfool/FlaskBook/blob/master/app.py
    
    requestor_id = Pending_Friend_Requests.query.filter_by(user_request_sent_from == user_id).first()
    
    new_friends = Friends(user_id=g.user, friend_user_id=requestor_id)
    
    
    
    db.session.add(new_friends)
    db.session.commit(new_friends)
    
    delete_requestor_id = Pending_Friend_Requests.query.filter_by(user_request_sent_from == user_id).first().delete()
    
    db.session.add(delete_requestor_id)
    db.session.commit(delete_requestor_id)
    
    return render_template('users/details.html')

@app.route('/delete_friend_request/<int:user_id>', methods=['POST'])
def delete_friend_request():
    
    """deleting friend request"""
    
    delete_requestor_id = Pending_Friend_Requests.query.filter_by(user_request_sent_from == user_id).first().delete()
    
    db.session.add(delete_requestor_id)
    db.session.commit(delete_requestor_id)
    
    return render_template('users/details.html')
    
########################################################################################################  

# @app.route('/default-pic')
# def default_pic():
#     """sending default-pic"""
    
#     return render_template('/static/images/default-pic')
    

########################################################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask
# information regarding turning off caching is from Springboard

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req