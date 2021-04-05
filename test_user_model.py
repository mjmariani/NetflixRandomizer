import os
import tempfile

from unittest import TestCase
from sqlalchemy import exc, or_, and_
from flask_bcrypt import Bcrypt
from flask import Flask, render_template, request, flash, redirect, session, g, abort

from .models import *
##from flask_sqlalchemy import SQLAlchemy

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql://postgres:postgres@localhost:5432/randomizer_test"

from app import app

## Test User model
class UserModelTestCase(TestCase):
    """Tests for User Model"""
    
    def setUp(self):
        """Clean up any existing users. Then, create test client, and add sample data."""
        db.drop_all()
        db.create_all()
        
        u1 = Users.signup("Jeffrey", "Johnson", "johnson@gmail.com")
        db.session.add(u1)
        db.session.flush()
        
        u2 = Users.signup("Marcy", "Rogers", "marcyrogers@outlook.com")
        db.session.add(u2)
        db.session.flush()
        
        db.session.commit()

        u1 = Users.query.get(1)
        u2 = Users.query.get(2)
        
        self.u1 = u1
        self.u2 = u2
        
        self.client = app.test_client()
        
    def tearDown(self):
        """Clean up any bad sql transaction"""
        res = super().tearDown()
        db.session.rollback()
        
    def test_user_model(self):
        """Does basic model work?"""

        u = Users.signup('John', 'Johnson', 'john@gmail.com')

        db.session.add(u)
        db.session.commit()

        # User should have no friends, no photo, no liked genres, no pending friend requests, and no movies in queue
        self.assertEqual(Users.query.filter(Users.first_name=='John').first().friends.count(), 0)
        self.assertEqual(Users.query.filter(Users.first_name=='John').first().user_photo.count(), 0)   
        self.assertEqual(Users.query.filter(Users.first_name=='John').first().genres_liked.count(), 0)  
        self.assertEqual(Users.query.filter(Users.first_name=='John').first().pending_friends_request.count(), 0)  
        self.assertEqual(Users.query.filter(Users.first_name=='John').first().queue.count(), 0)
     
        
    ##Signup() Tests
    def test_valid_signup(self):
        new_user = Users.signup("James","Kilk","kilk@gmail.com")
        db.session.add(new_user)
        db.session.commit()
        
        new_user = Users.query.filter(Users.first_name == 'James').first()
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.last_name, "Kilk")
        self.assertEqual(new_user.email, "kilk@gmail.com")
        self.assertTrue(type(new_user.user_id) is int)
    
    # def test_signup_missing_first_name(self):
    #     invalid = User.signup(None, None, None)
    #     with self.assertRaises(exc.IntegrityError) as context:
    #         db.session.commit()
            
    ##add authentication to user
    def add_authentication_to_user(self):
        user = self.u1
        bcrypt = Bcrypt()
        pass_hash = bcrypt.generate_password_hash("pass_hash").decode('UTF-8')
        auth = Authentication("chrome2x", pass_hash, user.user_id)
        db.session.add(auth)
        db.session.commit()
        self.u1.username = "chrome2x"
        self.u1.password = pass_hash
        auth_query = Authentication.query.filter(Authentication.user_id == user.user_id).first()
        self.assertIsNotNone(auth_query)
        self.assertEqual(auth_query.username, "chrome2x")
        self.assertEqual(auth_query.password_hash, pass_hash)
    
    def invalid_authentication_to_user(self):
        user = self.u2
        auth = Authentication(None, None, user.user_id)    
        db.session.add(auth)
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
            
    def invalid_authentication_to_user2(self):
        user = self.u2        
        auth_query = Authentication.query.filter(user_id == user.user_id).first()
        self.assertIsNone(auth_query)
        
    def add_authentication_with_missing_password(self):
        user = self.u2
        auth = Authentication("firefox", None, user.user_id)    
        db.session.add(auth)
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    ##Authentication Tests
    
    def test_valid_authentication(self):
        user = Users.signup("Jon", "Peter", "peter@gmail.com")
        db.session.add(user)
        db.session.flush()
        user = Users.query.filter(Users.first_name == "Jon").first()
        bcrypt = Bcrypt()
        pass_hash = bcrypt.generate_password_hash("pass").decode('UTF-8')
        auth = Authentication(username = "chrome2x", password_hash = pass_hash, user_id = user.user_id)
        db.session.add(auth)
        db.session.commit()
        u = Authentication.authenticate('chrome2x', 'pass')
        self.assertTrue(u)
        
    
    def test_invalid_username(self):
        pass_hash = bcrypt.generate_password_hash("pass_hash").decode('UTF-8')
        self.assertFalse(Authentication.authenticate("bad_username", pass_hash))

    def test_wrong_password(self):
        self.assertFalse(Authentication.authenticate("chrome2x", "bad_password"))
        
    ##add pending friend requests
    def add_pending_friend_request(self):
        request = Pending_Friend_Requests(self.u1.user_id, self.u2.user_id)
        db.session.add(request)
        db.session.commit()
        query_for_request = Pending_Friend_Requests.query.all()
        self.assertEqual(query_for_request.count(), 1)
    
    ##delete pending friend requests
    def delete_pending_friend_request(self):
        request = Pending_Friend_Requests.query.filter(Pending_Friend_Requests.id == 1).first().delete()
        db.session.add(request)
        db.session.commit()
        query_for_request = Pending_Friend_Requests.query.all()
        self.assertEqual(query_for_request.count(), 0)
        
    ##add friends
    def add_friend(self):
        request = Pending_Friend_Requests(self.u1.user_id, self.u2.user_id)
        db.session.add(request)
        db.session.flush()
        query_for_request = Pending_Friend_Requests.query.all()
        self.assertEqual(query_for_request.count(), 1)
        new_friend = Friends(self.u1.user_id, self.u2.user_id)
        db.session.add(new_friend)
        db.session.flush()
        ##db.session.refresh()
        new_friend = Friends.query.all()
        new_friend_row = Friends.query.get(1)
        db.session.add(Pending_Friend_Requests.query.filter(Pending_Friend_Requests.user_request_sent_from == self.u1.user_id).first().delete())
        db.session.commit()
        self.assertEqual(Pending_Friend_Requests.query.all().count(),0)
        self.assertEqual(new_friend.count(), 1)
        self.assertEqual(new_friend_row.user_id_1 == self.u1.user_id)
        self.assertEqual(new_friend_row.user_id_2 == self.u2.user_id)
    
    ##delete friends
    def delete_friend(self):
        delete_friend = Friends.query.filter(Friends.user_id_2 == self.u2.user_id).first().delete()
        db.session.add(delete_friend)
        db.session.commit()
        self.assertEqual(Friends.query.filter(Friends.user_id_2 == self.u2.user_id).count(),0)
    
    ##edit user info (add photo, change info)
    def edit_user_info(self):
        setattr(self.u1, 'first_name', 'Kevin')
        self.assertEqual(self.u1.first_name, "Kevin")
        setattr(self.u1, 'details', 'yo')
        self.assertEqual(self.u1.details, 'yo')
    
    ##add genres liked
    def add_genres_liked(self):
        user = self.u1
        genre = Genres("Action")
        db.session.add(genre)
        db.session.flush()
        genre_id = Genres.query.filter(Genres.name == "Action").first().id
        genre_name = Genres.query.filter(Genres.name == "Action").first().name
        liked_genre = Liked_Genres(genre_id, user.user_id, genre_name)
        db.session.add(liked_genre)
        db.session.commit()
        self.assertTrue(Liked_Genres.query.all().count(), 1)
        self.assertTrue(Liked_Genres.query.filter(Liked_Genres.genre_id == genre_id).first(), 1)
        self.assertTrue(Liked_Genres.query.filter(Liked_Genres.genre_id == genre_id).first().name, "Action")
        self.assertTrue(type(Liked_Genres.query.filter(Liked_Genres.genre_id == genre_id).first().id) is int)
    
    ##delete genres liked
    def delete_genres_liked(self):
        user = self.u1
        delete_genre = Liked_Genres.query.filter(Liked_Genres.genre_id == genre_id).first().delete()
        db.session.add(delete_genre) 
        db.session.commit()
        self.assertTrue(Liked_Genres.query.all().count(), 0)   
    
    def add_to_queue(self):
        user = self.u1
        movie = Movies("Springboarding", "IMDB", "123")
        db.session.add(movie)
        db.session.flush()
        movie_id = Movies.query.filter(Movies.name == "Springboarding").first().id
        tv_show = TV_Shows("Avatar The Last Airbender Animated Series", "TVIMDB", "546")
        db.session.add(tv_show)
        db.session.flush()
        tv_show_id = TV_Shows.query.filter(TV_Shows.name == "Avatar The Last Airbender Animated Series").first().id
        queue_1 = Queue(user.user_id, movie_id)
        db.session.add(queue_1)
        db.session.flush()
        self.assertTrue(Queue.query.all().count(), 1)
        self.assertTrue(Queue.query.filter(Queue.user_id == user.user_id).first().user_id, user.user_id)
        self.assertTrue(Queue.query.filter(Queue.user_id == user.user_id).first().movie_id, movie_id)
        queue_2 = Queue(user.user_id, tv_show_id)
        db.session.add(queue_2)
        db.session.commit()
        self.assertTrue(Queue.query.all().count(), 2)
        self.assertTrue(Queue.query.filter(and_(Queue.user_id == user.user_id, Queue.tv_show_id == tv_show_id)).first().count(), 1)