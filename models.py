"""SQLAlchemy models for Netflix Randomizer."""

from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class Users(db.Model):
    """User in the system."""
    
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    
    user_id = db.Column(db.Integer, primary_key=True, 
                   nullable=False, unique=True, 
                   autoincrement=True)
    
    first_name = db.Column(db.String(), nullable=True)
    
    last_name = db.Column(db.String(), nullable=True)
    
    created_at = db.Column(db.DateTime, nullable=False, 
                           default=datetime.utcnow())
    
    country_code = db.Column(db.Integer, db.ForeignKey('country.id', ondelete='CASCADE'), nullable=True)
    
    region_code = db.Column(db.Integer, db.ForeignKey('region.id', ondelete='CASCADE'), nullable=True)
    
    state_code = db.Column(db.Integer, db.ForeignKey('state.id', ondelete='CASCADE'), nullable=True)
    
    province_code = db.Column(db.Integer, db.ForeignKey('province.id', ondelete='CASCADE'), nullable=True)
    
    city_code = db.Column(db.Integer, db.ForeignKey('city.id', ondelete='CASCADE'), nullable=True)
    
    ##auth_id = db.Column(db.Integer, db.ForeignKey('auth.auth_id'), nullable=False, ondelete='cascade')
    
    email = db.Column(db.String(), nullable=True)
    
    
    gender_id = db.Column(db.Integer, nullable=True)
    
    details = db.Column(db.Text, nullable=True)
    
    ##confirmation_code = db.Column(db.String(), nullable=False)
    
    ##confirmation_time = db.Column(db.DateTime, default=datetime.utcnow())
    
    
    ##Using the 'likes' table as an intermediary table between the users and liked shows/movies
    
    tv_show_likes = db.relationship('TV_Shows', secondary='likes', back_populates="users", cascade="all, delete")
    
    movie_likes = db.relationship('Movies', secondary='likes', back_populates="users", cascade="all, delete")
    
    ##Using the 'friends' table as an intermediary table between the users who are friends with each other
    
    friends = db.relationship("Users", secondary='friends', back_populates="users", cascade="all, delete")
    
    credentials = db.relationship("Authentication", back_populates="users", cascade="all, delete")
    
    user_photo = db.relationship("User_Photos", back_populates="users", cascade="all, delete")
    
    genres_liked = db.relationship("Genres", secondary="liked_genres", back_populates="users", cascade="all, delete")
    
    pending_friends_request = db.relationship("Users", secondary="pending_friend_requests", cascade="all, delete")
    
    def __repr__(self):
        return f"<User #{self.user_id}: {self.credentials.username}, {self.email}>"
    
    def is_friends(self, other_user):
        """Are these 2 users friends?"""
        
        found_friend_list = [user for user in self.friends if user == other_user]
        return len(found_friend_list) == 1
    
    @classmethod
    def signup(cls, username, first_name, last_name, email, password, image_url):
        """Sign up the user.

        Args:
            username ([String]): [user's username]
            email ([String]): [user's email]
            password ([String]): [user's password]
            image_url ([text]): [url of image]
            first_name ([String]): [user's first name]
            last_name ([String]): [user's last name]
        """
        
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        
        user = Users(
            first_name = first_name,
            last_name = last_name,
            email = email
        )
        
        authentication_info = Authentication(
            username = username,
            password_hash = hashed_pwd,
            ##password_salt = pwd_salt
        )
        
        user_image = User_Photos(
            image_url = image_url

        )
    
        db.session.add(user, authentication_info, user_image)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`. 
        
        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """
        
        user = cls.query.filter_by(Users.credentials.has(username=username)).first()
        
        if user:
            is_auth = bcrypt.check_password_hash(user.credentials.password_hash, password)
            if is_auth:
                return user
        return False    
    

class Authentication(db.Model):
    """authentication table"""
    
    __tablename__ = 'auth'
    __table_args__ = {'extend_existing': True}
    
    auth_id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True, autoincrement=True)
    
    username = db.Column(db.String(), nullable=False)
    
    password_hash = db.Column(db.String(), nullable=False)
    
    ##password_salt = db.Column(db.String(), nullable=False)
    
    created_at = db.Column(db.DateTime, nullable=False, 
                           default=datetime.utcnow())
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
  
  ##Parts of code below on the Pending_Friend_Request table was influenced from source: https://github.com/logicfool/FlaskBook/blob/master/app.py  
class Pending_Friend_Requests(db.Model):
    __tablename__ = "pending_friend_requests"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_request_sent_from = db.Column(db.String)
    user_request_sent_to = db.Column(db.String)
    
    
class Country(db.Model):
    """country table"""
    
    __tablename__ = 'country'
    
    id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True, autoincrement=True)
    
    name = db.Column(db.String(), nullable=True)
    
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=True)
    
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=True)
    
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=True)
    
    province_id = db.Column(db.Integer, db.ForeignKey('province.id'), nullable=True)
    
    
class City(db.Model):
    
    __tablename__ = 'city'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    
    name = db.Column(db.String(), nullable=False)
    
    
class Region(db.Model):
    """region table"""
    
    __tablename__ = 'region'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    
    name = db.Column(db.String(), nullable=False)
    
    
class State(db.Model):
    """state table """
    
    __tablename__ = 'state'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    
    name = db.Column(db.String(), nullable=False)


class Province(db.Model):
    """province table"""
    
    __tablename__ = 'province'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    
    name = db.Column(db.String(), nullable=False)
    
class Movies(db.Model):
    """Movies table: for keeping track of the movies in user's queue, likes, etc"""
    
    __tablename__ = 'movies'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    
    name = db.Column(db.String())
    
    API_used = db.Column(db.String(), nullable=False)
    
    API_id = db.Column(db.String(), nullable=False
                       )   
    
class TV_Shows(db.Model):
    """TV Shows table: for keeping track of the tv shows in user's queue, likes, etc"""
    
    __tablename__ = 'tv_shows'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    
    name = db.Column(db.String())
    
    API_used = db.Column(db.String(), nullable=False)
    
    API_id = db.Column(db.String(), nullable=False
                       )           
        
class Queue(db.Model):
    """Table listing out movies/tv shows in queue for users"""
    
    __tablename__ = 'queue'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=True)
    
    tv_show_id = db.Column(db.Integer, db.ForeignKey('tv_shows.id'), nullable=True)
    
    
class User_Photos(db.Model):
    """table for storing user images/profile picture"""
    
    __tablename__ = 'user_photo'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    
    image_url = db.Column(db.Text, nullable=True, default="/static/images/default-pic.png")
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
class Liked_Genres(db.Model):
    """table to keep track of user's liked genres in order to make recommendations"""
    
    
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'liked_genres'
    
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    
    name = db.Column(db.String(), nullable=True)
    
    details = db.Column(db.String(), nullable=True)
    
class Genres(db.Model):
    """table for genres"""
    
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'genres'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    
    name = db.Column(db.String(), nullable=False)
    
    details = db.Column(db.String(), nullable=True)
    
class Friends(db.Model):
    """To keep track of user's relationship with other users"""
    
    __tablename__ = 'friends'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True, unique=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    friend_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    date_start = db.Column(db.DateTime, nullable=False, 
                           default=datetime.utcnow())
    
    
class Likes(db.Model):
    """To keep track of likes for users"""
    
    __tablename__ = 'likes'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    liked = db.Column(db.Boolean, nullable=True)
    
    watched = db.Column(db.Boolean, nullable=True)
    
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=True)
    
    tv_show_id = db.Column(db.Integer, db.ForeignKey('tv_shows.id'), nullable=True)
    
    date_liked = db.Column(db.DateTime, nullable=True, 
                           default=datetime.utcnow())
    
#     class Liked_Actors(db.Model):
#     """table to keep track of user's liked genres in order to make recommendations"""
    
#     __tablename__ = 'liked_genres'
    
#     id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    
#     genre_id = db.Column(db.Integer, db.ForeignKey('Genres.id'))
    
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    
#     name = db.Column(db.String(), nullable=True)
    
#     details = db.Column(db.String(), nullable=True)
    
# class Genres(db.Model):
#     """table for genres"""
    
#     __tablename__ = 'liked_genres'
    
#     id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    
#     name = db.Column(db.String(), nullable=False)
    
#     details = db.Column(db.String(), nullable=True)
    
    
    
    
def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
    ##return app