import os

from flask import Flask, render_template, request, flash, redirect, session, g, abort, url_for
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, login_required, logout_user, current_user, login_user, UserMixin, current_user
from flask_bootstrap import Bootstrap
from .forms import *
from .models import *


# if __name__ == '__main__':
#     app.run(host='localhost', port=5000)
CURR_USER_KEY = "curr_user"



# def create_app():
#     app = Flask(__name__)
#     app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#     db.init_app(app)
    
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0




#app.config['TESTING'] = True
#app.testing = True

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/randomizer'))

##app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/randomizer'

##Heroku Database URI:
##app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://aabvgpkkdnoded:062bfc6ff018204e4b75d64bfe78bf634c11adbf0395fdd6dfeb7c87a6033c4c@ec2-52-45-73-150.compute-1.amazonaws.com:5432/dek8pep0m2o9hq'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or "postgresql://postgres:postgres@localhost:5432/randomizer"


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "this really needs to be changed")

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)

##app.run(use_reloader=True)
#toolbar = DebugToolbarExtension(app)


bootstrap = Bootstrap(app)

connect_db(app)
# db.drop_all()
# db.create_all()



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
    
    friend_count = user.friends.count()
    
    username = user.credentials.first().username
    
    photo = user.user_photo.first().image_url
    if photo == '':
        photo = "../static/images/default-pic.png"
    
    queue = db.session.query(Queue).filter(Queue.user_id == user_id).all()
    
    videos = []
    
    for video in queue:
        if video.movie_id:
            
            movie = db.session.query(Movies).filter(id==video.movie_id).first()
            videos.append(movie)
        if video.tv_show_id:
            tv_show = db.session.query(TV_Shows).filter(id==video.tv_show_id).first()
            videos.append(tv_show)
    
    if request.method == "DELETE":
        try:
            ##queue = Queue.query.filter(user_id == user_id)
            id_to_delete = request.args.id
            video_to_delete = db.session.query(Queue).filter(id == id_to_delete)
            db.session.delete(video_to_delete)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            flash(error, error)
            
            
    return render_template('users/details.html', user=user, friends=friends,
                        username=username, photo=photo, friend_count = friend_count, queue = queue, videos = videos), 200

@app.route('/edit', methods=["GET", "POST"])
def edit():
    """edit user information"""
    form = UserEditForm(request.form)
    user = g.user
    user_id = g.user.user_id
    username = g.user.credentials.first().username
    country = ""
    city = ""
    province = ""
    state = ""
    
    if request.method=='GET':
        try:
            country = db.session.query(Country).filter(Country.id == (db.session.query(Users).filter(Users.user_id == user_id).first().country_code)).first() 
            city = db.session.query(City).filter(City.id == (db.session.query(Users).filter(Users.user_id == user_id).first().city_code)).first()
            province = db.session.query(Province).filter(Province.id == (db.session.query(Users).filter(Users.user_id == user_id).first().province_code)).first()
            state = db.session.query(State).filter(State.id == (db.session.query(Users).filter(Users.user_id == user_id).first().state_code)).first()
            
        except Exception as error:
            print(error)
    
    if request.method=='POST' and form.validate_on_submit():
        try:
            user_info_update = db.session.query(Users).get(user_id)
            props = {'first_name': form.firstName.data,
                     'last_name': form.lastName.data,
                     'email': form.email.data,
                     }
            
            for key, value in props.items():
                setattr(user_info_update, key, value)
            db.session.flush() 
            db.session.refresh()
            if form.picture.data:    
                picture_update = db.session.query(User_Photos).get(user_id)
                picture_props = {'image_url': form.picture.data}
            
                for key, value in picture_props.items():
                    setattr(picture_update, key, value)
                db.session.flush()
                db.session.refresh()
            
            if form.country.data: 
                country = ""
            
                if db.session.query(Country).filter(Country.name == form.country.data) != None:
                    country = db.session.query(Country).filter_by(Country.name == form.country.data)
                else:
                    country = Country(name = form.country.data)
                db.session.add(country)
                db.session.flush()
                db.session.refresh()
                countryId = db.session.query(Country).filter(Country.name == form.country.data).first().id
                other_user_props = {'country_code': countryId 
                                }
            
                for key, value in other_user_props.items():
                    setattr(user_info_update, key, value)
            
                db.session.flush()
                db.session.refresh()
                db.session.commit()
            
            if form.city.data:    
                city = ""
            
                if db.session.query(City).filter(City.name == form.city.data) != None:
                    city = db.session.query(City).filter_by(City.name == form.city.data)
                else:
                    city = City(name = form.city.data)
                db.session.add(city)
                db.session.flush()
                db.session.refresh()
                cityId = db.session.query(City).filter(City.name == form.city.data).first().id
                
                other_user_props = {'city_code': cityId}
            
                for key, value in other_user_props.items():
                    setattr(user_info_update, key, value)
            
                db.session.flush()
                db.session.refresh()
                db.session.commit()
            
            if form.state.data:    
                state = ""
            
                if db.session.query(State).filter(State.name == form.state.data) != None:
                    state = db.session.query(State).filter_by(State.name == form.state.data)
                else:
                    state = State(name = form.state.data)
                db.session.add(state)
                db.session.flush()
                db.session.refresh()
                stateId = db.session.query(State).filter(State.name == form.state.data).first().id
            
                other_user_props = {'state_code': stateId}
            
                for key, value in other_user_props.items():
                    setattr(user_info_update, key, value)
            
                db.session.flush()
                db.session.refresh()
                db.session.commit()
            
            if form.province.data:    
                province = ""
            
                if db.session.query(Province).filter(Province.name == form.province.data) != None:
                    province = db.session.query(Province).filter_by(Province.name == form.province.data)
                else:
                    province = Province(name = form.province.data)
                db.session.add(province)
                db.session.flush()
                db.session.refresh()
                provinceId = db.session.query(Province).filter(Country.name == form.province.data).first().id
                other_user_props = {
                                'province_code': provinceId,
                                }
                for key, value in other_user_props.items():
                    setattr(user_info_update, key, value)
            
                db.session.flush()
                db.session.refresh()
                db.session.commit()
            
            if form.password.data:
                authentication_update = db.session.query(Authentication).filter(Authentication.user_id == user_id)
                hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
                props = {'username': form.username.data,
                    'password': hashed_pwd}
            
                for key, value in props.items():
                    setattr(user_info_update, key, value)
                db.session.flush()    
                db.session.refresh()

            return redirect('/users/<int:user_id>'), 302
        
        except Exception as error:
            db.session.rollback()
            flash(error, error)
    
    return render_template('users/edit.html', form=form, user = user, country=country, state=state, province=province, city = city, username = username ), 200

@app.route('/friend_detail/<int:user_id>')
def friend_detail(user_id):
    
    """friend's details"""
    
    friend = db.session.query(Users).filter(Users.user_id == user_id).first()
    friend_count = friend.friends.count()
    photo = friend.user_photo.first().image_url
    if photo is None:
        photo = "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=crop&amp;w=500&amp;q=80"
    
    return render_template('/users/friend_detail.html', friend = friend, friend_count = friend_count, photo = photo)


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
            return redirect(url_for('details', user_id = user.user_id), 302)

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
            if form.username.data == "" or form.password.data == "":
                flash("Username and Password can't be blank.", 'danger')
                return render_template('/users/signup.html', form=form), 400
                
            user = Users.signup(
                
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                
                email=form.email.data,
                
                
                
            )
            
            ##db.session.commit()
            db.session.add(user)
            db.session.flush()
            
            # user = Users.query.order_by(Users.user_id.desc()).first()
            
            hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
            
            auth = Authentication(username = form.username.data, password_hash=hashed_pwd, user_id=user.user_id)
            
            db.session.add(auth)
            db.session.flush()
            ##db.session.refresh(auth)
            
            ##db.session.commit()
            
            user_image = User_Photos(
            image_url = form.image_url.data,
            user_id = user.user_id

            )
            db.session.add(user_image)
            db.session.flush()
            db.session.commit()
            
            
            do_login(user)
            ##import pdb; pdb.set_trace()
            
            flash("Registration successful!")
            
            ##html_dir = '/users/' + str(user.user_id)
            
            return redirect(url_for('details', user_id = user.user_id), 302)
            
        except Exception as error:
            db.session.rollback()
            ##print(error)
            return render_template('/users/signup.html', form=form, error=error), 400
    
    return render_template('/users/signup.html', form=form), 200

@app.route('/show', methods=["GET", "POST", "PUT"])
def show():
    
    """To show and run the netflix randomizer"""
    ##Only the GET and POST methods are implemented
    
    form = GenresLikedEditForm(request.form)
    flash('Please select filter preferences below', 'info')
    
    if request.method =='POST': 
        import json
        data = json.loads(str(request.get_json()))
        if data.like == 'True':
            
            try:
                if request.data.type == 'Movies':
                    movie = Movies(
                        name = data.name,
                        API_id = data.id,
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
                    name = data.name,
                    API_id = data.id,
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

    return render_template('/users/show.html', form=form), 200



########################################################################################################
#Homepage and error pages

@app.route('/')
def home():
    """Show homepage
    """
    
    return render_template('home.html'), 201

@app.route('/home')
def home_page():
    
    return redirect('/')

########################################################################################################
#Accepting Friend Requests and Deleting Friend requests


@app.route('/add_friend/<int:user_id>', methods=['POST'])
def accept_friend_request(user_id):
    """accepting friend's request"""
    
    ##Used the following code for help in setting this code: https://github.com/logicfool/FlaskBook/blob/master/app.py
    
    requestor_id = Pending_Friend_Requests.query.filter(Pending_Friend_Requests.user_request_sent_from == user_id).first()
    
    new_friends = Friends(user_id_1=g.user.user_id, user_id_2=requestor_id.user_request_sent_from)
    
    
    
    db.session.add(new_friends)
    db.session.commit(new_friends)
    
    delete_requestor_id = Pending_Friend_Requests.query.filter(Pending_Friend_Requests.user_request_sent_from == user_id).first().delete()
    
    db.session.add(delete_requestor_id)
    db.session.commit(delete_requestor_id)
    user_id = g.user.user_id
    return redirect(url_for('details', user_id = g.user.user_id), 302)

@app.route('/delete_friend_request/<int:user_id>', methods=['POST'])
def delete_friend_request(user_id):
    
    """deleting friend request"""
    
    delete_requestor_id = Pending_Friend_Requests.query.filter(Pending_Friend_Requests.user_request_sent_from == user_id).first().delete()
    
    db.session.add(delete_requestor_id)
    db.session.commit(delete_requestor_id)
    
    return redirect(url_for('details', user_id = g.user.user_id), 302)
    
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

