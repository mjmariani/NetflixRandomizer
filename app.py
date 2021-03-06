import os

from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, login_required, logout_user, current_user, login_user, UserMixin, current_user
from flask_bootstrap import Bootstrap

from forms import *
from models import *

CURR_USER_KEY = "curr_user"



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


bootstrap = Bootstrap(app)

connect_db(app)
##db.drop_all()
##db.create_all()

# @app.before_request
# def add_user_to_g():
#     """adding user to global object. If we're logged in, add curr user to Flask global."""
#     session[CURR_USER_KEY] = 1
#     g.user = Users.query.get(session[CURR_USER_KEY])
    
########################################################################################################
#User signup/login/logout
##The bottom code for before request, login, logout come from Springboard warbler project code

@app.before_request
def add_user_to_g():
    """adding user to global object. If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = Users.query.get(session[CURR_USER_KEY])
        
    else:
        g.user = None
        
def do_login(user):
    """Log in user."""
    
    session[CURR_USER_KEY] = user.user_id ##this is the user id of the user
    # import pdb; pdb.set_trace()
    add_user_to_g()
    
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

##the route below gets the details page, posts to details page (not implemented yet), and deletes queue items
@app.route('/users/<int:user_id>', methods=["GET", "POST", "DELETE"])
def details(user_id):
    """Show profile details page"""
    
    user = Users.query.get_or_404(user_id)
    
    friends = user.friends.all()
    
    friend_count = len(friends)
    
    username = user.credentials.first().username
    
    photo = user.user_photo.first().image_url
    
    queue = Queue.query.filter(user_id == user_id)
    
    videos = []
    
    for video in queue:
        if video.movie_id:
            
            movie = Movies.query.filter(id==video.movie_id).first()
            videos.append(movie.name)
        if video.tv_show_id:
            tv_show = TV_Shows.query.filter(id==video.tv_show_id).first()
            videos.append(tv_show.name)
    
    if request.method == "DELETE":
        try:
            ##queue = Queue.query.filter(user_id == user_id)
            id_to_delete = request.args.id
            video_to_delete = Queue.query.filter(id == id_to_delete)
            db.session.delete(video_to_delete)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            flash(error, error)
            
            
    return render_template('users/details.html', user=user, friends=friends,
                        username=username, photo=photo, friend_count = friend_count, queue = queue, videos = videos)

@app.route('/edit', methods=["GET", "POST"])
def edit():
    """edit user information"""
    
    user = g.user
    
    return render_template('users/edit.html', user = user)

@app.route('/friend_detail')
def friend_detail():
    
    """freind's details"""
    
    user = g.user
    
    return render_template('/users/friend_detail.html')


@app.route('/logout', methods=["GET"])
def logout():
    
    """to logout"""
    
    do_logout()
    
    return redirect('/')


@app.route('/login', methods=["GET", "POST"])
def login():
    
    """handle user login"""
    
    form = LoginForm(request.form)
    
    if request.method=='POST' and form.validate_on_submit():
        
        user = Authentication.authenticate(form.username.data,
                                 form.password.data)
            
        if user:
            do_login(user)
            ##flash(f"Hello, {Authentication.query.filter_by(user_id=int(user.user_id)).first().username}!", "success")
            return redirect("/details")

        flash("Invalid credentials.", 'danger')
    
    
    
    return render_template('/users/login.html', form=form)


@app.route('/signup', methods=["GET", "POST"])
def sign_up():
    """handle user sign up"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = SignupForm(request.form)
    
    if request.method=='POST' and form.validate_on_submit():
        
        try:
            user = Users.signup(
                
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                
                email=form.email.data,
                
                
                
            )
            
            ##db.session.commit()
            
            
            # user = Users.query.order_by(Users.user_id.desc()).first()
            
            hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
            
            auth = Authentication(username = form.username.data, password_hash=hashed_pwd, user_id=user.user_id)
            
            db.session.add(auth)
            db.session.flush()
            db.session.refresh(auth)
            
            db.session.commit()
            
            user_image = User_Photos(
            image_url = form.image_url.data,
            user_id = user.user_id

            )
            db.session.add(user_image)
            db.session.commit()
            ##import pdb; pdb.set_trace()
            
            do_login(user)
            
            
            flash("Registration successful!")
            
            return redirect('/users/details.html')
            
        except Exception as error:
            db.session.rollback()
            ##print(error)
            return render_template('/users/signup.html', form=form, error=error)
    
    return render_template('/users/signup.html', form=form)

@app.route('/show', methods=["GET", "POST", "PUT"])
def show():
    
    """To show and run the netflix randomizer"""
    
    
    form = GenresLikedEditForm(request.form)
    flash('Please select filter preferences below', 'info')
    
    if request.method =='POST' and request.args.like == 'True':
        # import pdb; pdb.set_trace()
        try:
            if request.args.type == 'Movies':
                movie = Movies(
                        name = request.args.name,
                        API_id = request.args.id,
                    )
                db.session.add(movie)
                db.session.flush()
                db.session.refresh(movie)
                like = Likes(
                    user_id = g.user.user_id,
                    liked = True,
                    movie_id = movie.id,
                    )
                db.session.add(like)
                db.session.flush()
                db.session.refresh(like)
                queue = Queue(
                    user_id = g.user.user_id,
                    movie_id = movie.id,
                )
                db.session.commit()
                
            else: 
                tvShow = TV_Shows(
                    name = request.args.name,
                    API_id = request.args.id,
                )
                db.session.add(tvShow)
                db.session.flush()
                db.session.refresh(tvShow)
                like = Likes(
                    liked = True,
                    tv_show_id = tvShow.id,
                    user_id = g.user.user_id,
                )
                db.session.add(like)
                db.session.flush()
                db.session.refresh(like)
                queue = Queue(
                    user_id = g.user.user_id,
                    tv_show_id = tvShow.id,
                )
                db.session.commit()
        except Exception as error:
            db.session.rollback()
            flash(error, error)

    return render_template('/users/show.html', form=form)



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
    
    requestor_id = Pending_Friend_Requests.query.filter(user_request_sent_from == user_id).first()
    
    new_friends = Friends(user_id_1=g.user.user_id, user_id_2=requestor_id.user_request_sent_from)
    
    
    
    db.session.add(new_friends)
    db.session.commit(new_friends)
    
    delete_requestor_id = Pending_Friend_Requests.query.filter(user_request_sent_from == user_id).first().delete()
    
    db.session.add(delete_requestor_id)
    db.session.commit(delete_requestor_id)
    
    return render_template('users/details.html')

@app.route('/delete_friend_request/<int:user_id>', methods=['POST'])
def delete_friend_request():
    
    """deleting friend request"""
    
    delete_requestor_id = Pending_Friend_Requests.query.filter(user_request_sent_from == user_id).first().delete()
    
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