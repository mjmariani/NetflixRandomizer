import os
import tempfile

#import pytest
from unittest import TestCase

from app import app
from models import *

TEST_DB = "postgresql://postgres:postgres@localhost:5432/randomizer_test"


class RandomizerTestCase_1(TestCase):
    """Integration test for flask app"""
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB
        cls.app = app.test_client()
        db.drop_all()
        db.create_all()
        db.session.expire_on_commit = False
        ##cls.assertEqual(app.config.debug, False)
        u1 = Users.signup(first_name = "Jeffrey", last_name = "Johnson", email = "johnson@gmail.com")
        db.session.add(u1)
        db.session.flush()
        db.session.refresh(u1)
        db.session.expunge(u1)
        
        u2 = Users.signup(first_name = "Marcy", last_name = "Rogers", email = "marcyrogers@outlook.com")
        db.session.add(u2)
        db.session.flush()
        db.session.refresh(u2)
        db.session.expunge(u2)
        
        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt()
        pass_hash_1 = bcrypt.generate_password_hash("pass_hash_1").decode('UTF-8')
        auth_u1 = Authentication(username = "chrome2x", password_hash = pass_hash_1, user_id = u1.user_id)
        db.session.add(auth_u1)
        db.session.flush()
        pass_hash_2 = bcrypt.generate_password_hash("pass_hash_2").decode('UTF-8')
        auth_u2 = Authentication(username ="firefox2x", password_hash =pass_hash_2, user_id =u2.user_id)
        db.session.add(auth_u2)
        db.session.flush()

        db.session.commit()
        cls.u1 = u1
        cls.u2 = u2
        cls.u1.password = 'pass_hash_1'
        cls.auth_u1 = auth_u1
        cls.auth_u2 = auth_u2
        cls.u2.password = 'pass_hash_2'
    
    @classmethod   
    def tearDownClass(self):
        db.session.remove()
        db.drop_all()


    # def test_homepage_route(self):
    #     """Test homepage route."""
    #     with app.test_client() as client:
    #        res = client.get('/')
    #        html = res.get_data(as_text=True)
    #        self.assertEqual(res.status_code, 201)
    #        self.assertIn('<h1 class="display-4">Welcome to the Netflix Randomizer</h1>', html) 
    
    def test_homepage_route(self):
        """Test homepage route."""
        res = self.app.get('/')
        html = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 201)
        self.assertIn('<h1 class="display-4">Welcome to the Netflix Randomizer</h1>', html)

    def test_home_route(self):
        """Test homepage route."""
        res = self.app.get('/home')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.location, 'http://localhost/')
    
    def test_info_route(self):
        """Test info route."""
        res = self.app.get('/info')
        html = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('<a class="list-group-item list-group-item-action active" id="list-home-list" data-toggle="list" href="#list-home" role="tab" aria-controls="home">About</a>', html)

    def test_info_route(self):
        """Test sign up /get route."""
        res = self.app.get('/signup')
        html = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('<h1 class="h3 mb-3 font-weight-normal">Sign Up!</h1>', html) 

class RandomizerTestCase_2(TestCase):
    """Integration test for flask app"""
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB
        cls.app = app.test_client()
        db.drop_all()
        db.create_all()
        db.session.expire_on_commit = False
        ##cls.assertEqual(app.config.debug, False)
        u1 = Users.signup(first_name = "Jeffrey", last_name = "Johnson", email = "johnson@gmail.com")
        db.session.add(u1)
        db.session.flush()
        db.session.refresh(u1)
        db.session.expunge(u1)
        
        u2 = Users.signup(first_name = "Marcy", last_name = "Rogers", email = "marcyrogers@outlook.com")
        db.session.add(u2)
        db.session.flush()
        db.session.refresh(u2)
        db.session.expunge(u2)
        
        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt()
        pass_hash_1 = bcrypt.generate_password_hash("pass_hash_1").decode('UTF-8')
        auth_u1 = Authentication(username = "chrome2x", password_hash = pass_hash_1, user_id = u1.user_id)
        db.session.add(auth_u1)
        db.session.flush()
        pass_hash_2 = bcrypt.generate_password_hash("pass_hash_2").decode('UTF-8')
        auth_u2 = Authentication(username ="firefox2x", password_hash =pass_hash_2, user_id =u2.user_id)
        db.session.add(auth_u2)
        db.session.flush()

        db.session.commit()
        cls.u1 = u1
        cls.u2 = u2
        cls.u1.password = 'pass_hash_1'
        cls.auth_u1 = auth_u1
        cls.auth_u2 = auth_u2
        cls.u2.password = 'pass_hash_2'
    
    @classmethod   
    def tearDownClass(self):
        db.session.remove()
        db.drop_all()


    ##Not sure why this test is not passing; this is working when I run flask locally
    def test_info_route(self):
        """Test sign up /post route w/ valid data.""" 
        data = {"first_name": "James", "last_name":"Kirk",
        "username": "chrome5x", "email": "james@gmail.com", "password":"jeff34523646", 
        "image_url": "https://cdn.vox-cdn.com/thumbor/Yt1avchDkHqEqJuhYZ3YjKF3kFc=/0x0:1700x960/1200x675/filters:focal(714x344:986x616)/cdn.vox-cdn.com/uploads/chorus_image/image/57514059/mario.0.jpg"}
        res = self.app.post('/signup', data = data, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)
        self.assertIn('Registration successful!', html)
        self.assertIn('<h5 class="mb-0">Friends</h5>', html)
                
    def test_info_route(self):
        """Test sign up /post route w/ valid data (checking that it redirects).""" 
        data = {"first_name": "James", "last_name":"Kirk",
        "username": "chrome5x", "email": "james@gmail.com", "password":"jeff34523646", 
        "image_url": "https://cdn.vox-cdn.com/thumbor/Yt1avchDkHqEqJuhYZ3YjKF3kFc=/0x0:1700x960/1200x675/filters:focal(714x344:986x616)/cdn.vox-cdn.com/uploads/chorus_image/image/57514059/mario.0.jpg"}
        res = self.app.post('/signup', data = data)
        self.assertEqual(res.status_code, 302)
                
    def test_info_route(self):
        """Test sign up /post route w/ missing first_name data.""" 
        data = { "last_name":"Kirk",
        "username": "chrome5x", "email": "james@gmail.com", "password":"jeff34523646", 
        "image_url": "https://cdn.vox-cdn.com/thumbor/Yt1avchDkHqEqJuhYZ3YjKF3kFc=/0x0:1700x960/1200x675/filters:focal(714x344:986x616)/cdn.vox-cdn.com/uploads/chorus_image/image/57514059/mario.0.jpg"}
        res = self.app.post('/signup', data = data, follow_redirects=True)
        self.assertEqual(res.status_code, 400)
                
    def test_info_route(self):
        """Test sign up /post route w/ missing last_name data."""            
        data = {"first_name": "James",
        "username": "chrome5x", "email": "james@gmail.com", "password":"jeff34523646", 
        "image_url": "https://cdn.vox-cdn.com/thumbor/Yt1avchDkHqEqJuhYZ3YjKF3kFc=/0x0:1700x960/1200x675/filters:focal(714x344:986x616)/cdn.vox-cdn.com/uploads/chorus_image/image/57514059/mario.0.jpg"}
        res = self.app.post('/signup', data = data, follow_redirects=True)
        self.assertEqual(res.status_code, 400)

class RandomizerTestCase_3(TestCase):
    """Integration test for flask app"""
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB
        cls.app = app.test_client()
        db.drop_all()
        db.create_all()
        db.session.expire_on_commit = False
        ##cls.assertEqual(app.config.debug, False)
        u1 = Users.signup(first_name = "Jeffrey", last_name = "Johnson", email = "johnson@gmail.com")
        db.session.add(u1)
        db.session.flush()
        db.session.refresh(u1)
        db.session.expunge(u1)
        
        u2 = Users.signup(first_name = "Marcy", last_name = "Rogers", email = "marcyrogers@outlook.com")
        db.session.add(u2)
        db.session.flush()
        db.session.refresh(u2)
        db.session.expunge(u2)
        
        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt()
        pass_hash_1 = bcrypt.generate_password_hash("pass_hash_1").decode('UTF-8')
        auth_u1 = Authentication(username = "chrome2x", password_hash = pass_hash_1, user_id = u1.user_id)
        db.session.add(auth_u1)
        db.session.flush()
        pass_hash_2 = bcrypt.generate_password_hash("pass_hash_2").decode('UTF-8')
        auth_u2 = Authentication(username ="firefox2x", password_hash =pass_hash_2, user_id =u2.user_id)
        db.session.add(auth_u2)
        db.session.flush()

        db.session.commit()
        cls.u1 = u1
        cls.u2 = u2
        cls.u1.password = 'pass_hash_1'
        cls.auth_u1 = auth_u1
        cls.auth_u2 = auth_u2
        cls.u2.password = 'pass_hash_2'
    
    @classmethod   
    def tearDownClass(self):
        db.session.remove()
        db.drop_all()

               
    def test_info_route(self):
        """Test sign up /post route w/ invalid email data."""             
        data = {"first_name": "James", "last_name":"Kirk",
        "username": "chrome5x", "email": "james", "password":"jeff34523646", 
        "image_url": "https://cdn.vox-cdn.com/thumbor/Yt1avchDkHqEqJuhYZ3YjKF3kFc=/0x0:1700x960/1200x675/filters:focal(714x344:986x616)/cdn.vox-cdn.com/uploads/chorus_image/image/57514059/mario.0.jpg"}
        res = self.app.post('/signup', data = data, follow_redirects=True)
        self.assertEqual(res.status_code, 400)
    
    def test_info_route(self):
        """Test sign up /post route w/ missing email data.""" 
        data = {"first_name": "James", "last_name":"Kirk",
        "username": "chrome5x", "password":"jeff34523646", 
        "image_url": "https://cdn.vox-cdn.com/thumbor/Yt1avchDkHqEqJuhYZ3YjKF3kFc=/0x0:1700x960/1200x675/filters:focal(714x344:986x616)/cdn.vox-cdn.com/uploads/chorus_image/image/57514059/mario.0.jpg"}            
        res = self.app.post('/signup', data = data, follow_redirects=True)
        self.assertEqual(res.status_code, 400)
                
    def test_info_route(self):
        """Test sign up /post route w/ invalid password data.""" 
        data = {"first_name": "James", "last_name":"Kirk",
        "username": "chrome5x", "email": "james@gmail.com", "password":"jef", 
        "image_url": "https://cdn.vox-cdn.com/thumbor/Yt1avchDkHqEqJuhYZ3YjKF3kFc=/0x0:1700x960/1200x675/filters:focal(714x344:986x616)/cdn.vox-cdn.com/uploads/chorus_image/image/57514059/mario.0.jpg"}             
        res = self.app.post('/signup', data = data, follow_redirects=True)
        self.assertEqual(res.status_code, 400)
                
    def test_info_route(self):
        """Test sign up /post route w/ missing password data."""         
        data = {"first_name": "James", "last_name":"Kirk",
        "username": "chrome5x", "email": "james@gmail.com", "password":"", 
        "image_url": "https://cdn.vox-cdn.com/thumbor/Yt1avchDkHqEqJuhYZ3YjKF3kFc=/0x0:1700x960/1200x675/filters:focal(714x344:986x616)/cdn.vox-cdn.com/uploads/chorus_image/image/57514059/mario.0.jpg"}
        res = self.app.post('/signup', data = data, follow_redirects=True)
        self.assertEqual(res.status_code, 400)

class RandomizerTestCase_4(TestCase):
    """Integration test for flask app"""
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB
        cls.app = app.test_client()
        db.drop_all()
        db.create_all()
        db.session.expire_on_commit = False
        ##cls.assertEqual(app.config.debug, False)
        u1 = Users.signup(first_name = "Jeffrey", last_name = "Johnson", email = "johnson@gmail.com")
        db.session.add(u1)
        db.session.flush()
        db.session.refresh(u1)
        db.session.expunge(u1)
        
        u2 = Users.signup(first_name = "Marcy", last_name = "Rogers", email = "marcyrogers@outlook.com")
        db.session.add(u2)
        db.session.flush()
        db.session.refresh(u2)
        db.session.expunge(u2)
        
        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt()
        pass_hash_1 = bcrypt.generate_password_hash("pass_hash_1").decode('UTF-8')
        auth_u1 = Authentication(username = "chrome2x", password_hash = pass_hash_1, user_id = u1.user_id)
        db.session.add(auth_u1)
        db.session.flush()
        pass_hash_2 = bcrypt.generate_password_hash("pass_hash_2").decode('UTF-8')
        auth_u2 = Authentication(username ="firefox2x", password_hash =pass_hash_2, user_id =u2.user_id)
        db.session.add(auth_u2)
        db.session.flush()

        db.session.commit()
        cls.u1 = u1
        cls.u2 = u2
        cls.u1.password = 'pass_hash_1'
        cls.auth_u1 = auth_u1
        cls.auth_u2 = auth_u2
        cls.u2.password = 'pass_hash_2'
    
    @classmethod   
    def tearDownClass(self):
        db.session.remove()
        db.drop_all()


    def test_randomizer_route(self):
        """Test randomizer route after login /get"""
        with app.app_context():
            with self.app.session_transaction() as change_session:
                change_session['CURR_USER_KEY'] = self.u1.user_id
            res = self.app.get('/show')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Filter Selections</h1>', html)
                

    def test_randomizer_route(self):
        """Test randomizer route after login valid (no missing data) /post (liking a movie)"""
        with app.app_context():
            with self.app.session_transaction() as change_session:
                change_session['CURR_USER_KEY'] = self.u1.user_id
            from flask import json
            data = json.dumps({"like": "True",
                        "name":"innerText",
                        "id": "54"
            })
            res = self.app.post('/show', data=data, content_type='application/json')
            html = res.get_data(as_text=True)
            ##self.assertEqual(res.status_code, 200)
            self.assertNotIn('<div class="error" role="alert" id="messages">', html)
            ##self.assertIn('<div class="tinder--cards" >', html)
                
    def test_randomizer_route(self):
        """Test randomizer route after login valid (no missing data) /post (liking a tv show)"""
        with app.app_context():
            with self.app.session_transaction() as change_session:
                change_session['CURR_USER_KEY'] = self.u1.user_id
            from flask import jsonify
            from flask import json
            data = json.dumps({"like": "True",
                        "name":"innerText",
                        "id": "54"
            })
            res = self.app.post('/show', data=data, content_type='application/json')
            html = res.get_data(as_text=True)
            self.assertNotIn('<div class="error" role="alert" id="messages">', html)            

##Think in order to get good test coverage of /show, I will need to test on the client side as the this page is making external API calls on the client-side rather than back-end
##This is then done through mock testing
                
    def test_randomizer_route(self):
        """Test randomizer route after login invalid /post"""
        
        with app.app_context():
            with self.app.session_transaction() as change_session:
                change_session['CURR_USER_KEY'] = self.u1.user_id
            from flask import json
            data = json.dumps({"like": "True",
                        "name":"innerText",
                        "id": "54"
            })
            res = self.app.post('/show', data=data, content_type='application/json')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 400)
            self.assertIn('<div class="error" role="alert" id="messages">', html) 

class RandomizerTestCase_5(TestCase):
    """Integration test for flask app"""
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB
        cls.app = app.test_client()
        db.drop_all()
        db.create_all()
        db.session.expire_on_commit = False
        ##cls.assertEqual(app.config.debug, False)
        u1 = Users.signup(first_name = "Jeffrey", last_name = "Johnson", email = "johnson@gmail.com")
        db.session.add(u1)
        db.session.flush()
        db.session.refresh(u1)
        db.session.expunge(u1)
        
        u2 = Users.signup(first_name = "Marcy", last_name = "Rogers", email = "marcyrogers@outlook.com")
        db.session.add(u2)
        db.session.flush()
        db.session.refresh(u2)
        db.session.expunge(u2)
        
        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt()
        pass_hash_1 = bcrypt.generate_password_hash("pass_hash_1").decode('UTF-8')
        auth_u1 = Authentication(username = "chrome2x", password_hash = pass_hash_1, user_id = u1.user_id)
        db.session.add(auth_u1)
        db.session.flush()
        pass_hash_2 = bcrypt.generate_password_hash("pass_hash_2").decode('UTF-8')
        auth_u2 = Authentication(username ="firefox2x", password_hash =pass_hash_2, user_id =u2.user_id)
        db.session.add(auth_u2)
        db.session.flush()

        db.session.commit()
        cls.u1 = u1
        cls.u2 = u2
        cls.u1.password = 'pass_hash_1'
        cls.auth_u1 = auth_u1
        cls.auth_u2 = auth_u2
        cls.u2.password = 'pass_hash_2'
    
    @classmethod   
    def tearDownClass(self):
        db.session.remove()
        db.drop_all()


    def login_route(self):
        """Test login route works /get"""
        with app.app_context():
            res = self.app.get('/login')
            self.assertEqual(res.status_code, 200)

    def login_route(self):
        """Test login route works /post"""
        with app.app_context():
            data = {'username': self.auth_u1, 'password': self.u1.password}
            res = self.app.post('/login', data = data)
            self.assertEqual(res.status_code, 302)

    def login_route(self):
        """Test login route works /post follow redirect"""
        with app.app_context():
            data = {'username': self.auth_u1, 'password': self.u1.password}
            res = self.app.post('/login', data = data, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            self.assertIn('<h5 class="mb-0">Friends</h5>', html)

    def logout(self):
        """Test logout route"""
        with app.app_context():
            with self.app.session_transaction() as change_session:
                change_session['CURR_USER_KEY'] = self.u1.user_id
            res = self.app.get('/logout')
            self.assertEqual(res.status_code, 200)

class RandomizerTestCase_6(TestCase):
    """Integration test for flask app"""
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB
        cls.app = app.test_client()
        db.drop_all()
        db.create_all()
        db.session.expire_on_commit = False
        ##cls.assertEqual(app.config.debug, False)
        u1 = Users.signup(first_name = "Jeffrey", last_name = "Johnson", email = "johnson@gmail.com")
        db.session.add(u1)
        db.session.flush()
        db.session.refresh(u1)
        db.session.expunge(u1)
        
        u2 = Users.signup(first_name = "Marcy", last_name = "Rogers", email = "marcyrogers@outlook.com")
        db.session.add(u2)
        db.session.flush()
        db.session.refresh(u2)
        db.session.expunge(u2)
        
        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt()
        pass_hash_1 = bcrypt.generate_password_hash("pass_hash_1").decode('UTF-8')
        auth_u1 = Authentication(username = "chrome2x", password_hash = pass_hash_1, user_id = u1.user_id)
        db.session.add(auth_u1)
        db.session.flush()
        pass_hash_2 = bcrypt.generate_password_hash("pass_hash_2").decode('UTF-8')
        auth_u2 = Authentication(username ="firefox2x", password_hash =pass_hash_2, user_id =u2.user_id)
        db.session.add(auth_u2)
        db.session.flush()

        db.session.commit()
        cls.u1 = u1
        cls.u2 = u2
        cls.u1.password = 'pass_hash_1'
        cls.auth_u1 = auth_u1
        cls.auth_u2 = auth_u2
        cls.u2.password = 'pass_hash_2'
    
    @classmethod   
    def tearDownClass(self):
        db.session.remove()
        db.drop_all()


    def edit_route(self):
        """Test edit route /get"""
        with app.app_context():
            with self.app.session_transaction() as change_session:
                change_session['CURR_USER_KEY'] = self.u1.user_id
            res = self.app.get('/edit')
            self.assertEqual(res.status_code, 200)
                
    def edit_route(self):
        """Test edit route /post"""
        with app.app_context():
            with self.app.session_transaction() as change_session:
                change_session['CURR_USER_KEY'] = self.u1.user_id
        data = {
                    'first_name': 'Jameson',
                    'last_name': 'Kirkson',
                    'username': 'chrome3x',
                    'email': 'chrome34@outlook.com',
                    'image_url': '',
                    'country': 'Portugal',
                    'city': 'Lisbon',
                    'state': '',
                    'province': '',
                    'gender': 'male',
                    'details': '',
                    'password': 'pytesting'
                    }
        res = self.app.post('/edit', data=data)
        self.assertEqual(res.status_code, 302)

    def edit_route(self):
        """Test edit route /post follow redirect"""
        with app.app_context():
            with self.app.session_transaction() as change_session:
                change_session['CURR_USER_KEY'] = self.u1.user_id
        data = {
                    'first_name': 'Jameson',
                    'last_name': 'Kirkson',
                    'username': 'chrome3x',
                    'email': 'chrome34@outlook.com',
                    'image_url': '',
                    'country': 'Portugal',
                    'city': 'Lisbon',
                    'state': '',
                    'province': '',
                    'gender': 'male',
                    'details': '',
                    'password': 'pytesting'
                    }
        res = self.app.post('/edit', data=data, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
                
    def edit_route(self):
        """Test edit route /post missing required data"""
        with app.app_context():
            with self.app.session_transaction() as change_session:
                change_session['CURR_USER_KEY'] = self.u1.user_id
        data = {
                    'email': 'chrome34@outlook.com',
                    'image_url': '',
                    'country': 'Portugal',
                    'city': 'Lisbon',
                    'state': '',
                    'province': '',
                    'gender': 'male',
                    'details': '',
                    'password': 'pytesting'
                    }
        res = self.app.post('/edit', data=data)
        html = res.get_data(as_text=True)
        self.assertIn('<div class="error" role="alert" id="messages">', html) 

class RandomizerTestCase_7(TestCase):
    """Integration test for flask app"""
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB
        cls.app = app.test_client()
        db.drop_all()
        db.create_all()
        db.session.expire_on_commit = False
        ##cls.assertEqual(app.config.debug, False)
        u1 = Users.signup(first_name = "Jeffrey", last_name = "Johnson", email = "johnson@gmail.com")
        db.session.add(u1)
        db.session.flush()
        db.session.refresh(u1)
        db.session.expunge(u1)
        
        u2 = Users.signup(first_name = "Marcy", last_name = "Rogers", email = "marcyrogers@outlook.com")
        db.session.add(u2)
        db.session.flush()
        db.session.refresh(u2)
        db.session.expunge(u2)
        
        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt()
        pass_hash_1 = bcrypt.generate_password_hash("pass_hash_1").decode('UTF-8')
        auth_u1 = Authentication(username = "chrome2x", password_hash = pass_hash_1, user_id = u1.user_id)
        db.session.add(auth_u1)
        db.session.flush()
        pass_hash_2 = bcrypt.generate_password_hash("pass_hash_2").decode('UTF-8')
        auth_u2 = Authentication(username ="firefox2x", password_hash =pass_hash_2, user_id =u2.user_id)
        db.session.add(auth_u2)
        db.session.flush()

        db.session.commit()
        cls.u1 = u1
        cls.u2 = u2
        cls.u1.password = 'pass_hash_1'
        cls.auth_u1 = auth_u1
        cls.auth_u2 = auth_u2
        cls.u2.password = 'pass_hash_2'
    
    @classmethod   
    def tearDownClass(self):
        db.session.remove()
        db.drop_all()


    def edit_route(self):
        """Test edit route /post invalid email"""
        with app.app_context():
            with self.app.session_transaction() as change_session:
                change_session['CURR_USER_KEY'] = self.u1.user_id
        data = {
                    'first_name': 'Jameson',
                    'last_name': 'Kirkson',
                    'username': 'chrome3x',
                    'email': 'chrome34.com',
                    'image_url': '',
                    'country': 'Portugal',
                    'city': 'Lisbon',
                    'state': '',
                    'province': '',
                    'gender': 'male',
                    'details': '',
                    'password': 'pytesting'
                    }
        res = self.app.post('/edit', data=data)
        html = res.get_data(as_text=True)
        self.assertIn('<div class="error" role="alert" id="messages">', html)


##Test randomizer (movies are added to queue in db)

    ##Possibly test JS (client-side code) with jest
    
##Test that queue actually shows in detail page



