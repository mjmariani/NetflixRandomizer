import os
import tempfile

#import pytest
from unittest import TestCase
from flask import jsonify
from app import app
from models import *

os.environ['DATABASE_URL'] = "postgresql://postgres:postgres@localhost:5432/randomizer_test"

# @pytest.fixture
# def client():
#     db_fd, app.config['DATABASE'] = tempfile.mkstemp()
#     app.config['TESTING'] = True
    
#     with app.test_client() as client:
#         with app.app_context():
#             #app.init_db()
#             yield client
#         #yield client
#     os.close(db_fd)
#     os.unlink(app.config['DATABASE'])


class RandomizerTestCase_1(TestCase):
    """Integration tests (split into 2 classes) for flask app"""

    def setUp(self):
        db.drop_all()
        db.create_all()
        
        u1 = Users.signup("Jeffrey", "Johnson", "johnson@gmail.com")
        db.session.add(u1)
        db.session.flush()
        
        u2 = Users.signup("Marcy", "Rogers", "marcyrogers@outlook.com")
        db.session.add(u2)
        db.session.flush()
        
        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt()
        pass_hash_1 = bcrypt.generate_password_hash("pass_hash_1").decode('UTF-8')
        auth_u1 = Authentication("chrome2x", pass_hash_1, u1.user_id)
        db.session.add(auth_u1)
        db.session.flush()
        pass_hash_2 = bcrypt.generate_password_hash("pass_hash_2").decode('UTF-8')
        auth_u2 = Authentication("firefox2x", pass_hash_2, u2.user_id)
        db.session.add(auth_u2)
        db.session.flush()
        db.session.commit()
        self.u1 = u1
        self.u2 = u2
        self.u1.password = 'pass_hash_1'
        self.auth_u1 = auth_u1
        self.auth_u2 = auth_u2
        self.u2.password = 'pass_hash_2'
        
    def tearDown(self):
        db.drop_all()


    def test_homepage_route(self):
        """Test homepage route."""
        with app.test_client() as client:
           res = client.get('/')
           html = res.get_data(as_text=True)
           self.assertEqual(res.status_code, 201)
           self.assertIn('<h1 class="display-4">Welcome to the Netflix Randomizer</h1>', html) 

    def test_home_route(self):
        """Test homepage route."""
        with app.test_client() as client:
            res = client.get('/home')
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/')
    
    def test_info_route(self):
        """Test info route."""
        with app.test_client() as client:
            res = client.get('/info')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<a class="list-group-item list-group-item-action active" id="list-home-list" data-toggle="list" href="#list-home" role="tab" aria-controls="home">About</a>', html)

    def test_info_route(self):
        """Test sign up /get route."""
        with app.test_client() as client:
            res = client.get('/signup')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="h3 mb-3 font-weight-normal">Sign Up!</h1>', html) 

    ##Not sure why this test is not passing; this is working when I run flask locally
    def test_info_route(self):
        """Test sign up /post route w/ valid data.""" 
        with app.test_client() as client:
            with app.app_context():
                data = {"first_name": "James", "last_name":"Kirk",
                "username": "chrome5x", "email": "james@gmail.com", "password":"jeff34523646", 
                "image_url": "https://cdn.vox-cdn.com/thumbor/Yt1avchDkHqEqJuhYZ3YjKF3kFc=/0x0:1700x960/1200x675/filters:focal(714x344:986x616)/cdn.vox-cdn.com/uploads/chorus_image/image/57514059/mario.0.jpg"}
                res = client.post('/signup', data = data, follow_redirects=True)
                self.assertEqual(res.status_code, 200)
                html = res.get_data(as_text=True)
                self.assertIn('Registration successful!', html)
                self.assertIn('<h5 class="mb-0">Friends</h5>', html)
                
    def test_info_route(self):
        """Test sign up /post route w/ valid data (checking that it redirects).""" 
        with app.test_client() as client:
            with app.app_context():
                data = {"first_name": "James", "last_name":"Kirk",
                "username": "chrome5x", "email": "james@gmail.com", "password":"jeff34523646", 
                "image_url": "https://cdn.vox-cdn.com/thumbor/Yt1avchDkHqEqJuhYZ3YjKF3kFc=/0x0:1700x960/1200x675/filters:focal(714x344:986x616)/cdn.vox-cdn.com/uploads/chorus_image/image/57514059/mario.0.jpg"}
                res = client.post('/signup', data = data)
                self.assertEqual(res.status_code, 302)
                
    def test_info_route(self):
        """Test sign up /post route w/ missing first_name data.""" 
        with app.test_client() as client:
            with app.app_context():
                data = { "last_name":"Kirk",
                "username": "chrome5x", "email": "james@gmail.com", "password":"jeff34523646", 
                "image_url": "https://cdn.vox-cdn.com/thumbor/Yt1avchDkHqEqJuhYZ3YjKF3kFc=/0x0:1700x960/1200x675/filters:focal(714x344:986x616)/cdn.vox-cdn.com/uploads/chorus_image/image/57514059/mario.0.jpg"}
                res = client.post('/signup', data = data, follow_redirects=True)
                self.assertEqual(res.status_code, 400)
                
    def test_info_route(self):
        """Test sign up /post route w/ missing last_name data.""" 
        with app.test_client() as client:
            with app.app_context():            
                data = {"first_name": "James",
                "username": "chrome5x", "email": "james@gmail.com", "password":"jeff34523646", 
                "image_url": "https://cdn.vox-cdn.com/thumbor/Yt1avchDkHqEqJuhYZ3YjKF3kFc=/0x0:1700x960/1200x675/filters:focal(714x344:986x616)/cdn.vox-cdn.com/uploads/chorus_image/image/57514059/mario.0.jpg"}
                res = client.post('/signup', data = data, follow_redirects=True)
                self.assertEqual(res.status_code, 400)
                
    def test_info_route(self):
        """Test sign up /post route w/ invalid email data.""" 
        with app.test_client() as client:
            with app.app_context():            
                data = {"first_name": "James", "last_name":"Kirk",
                "username": "chrome5x", "email": "james", "password":"jeff34523646", 
                "image_url": "https://cdn.vox-cdn.com/thumbor/Yt1avchDkHqEqJuhYZ3YjKF3kFc=/0x0:1700x960/1200x675/filters:focal(714x344:986x616)/cdn.vox-cdn.com/uploads/chorus_image/image/57514059/mario.0.jpg"}
                res = client.post('/signup', data = data, follow_redirects=True)
                self.assertEqual(res.status_code, 400)
    
    def test_info_route(self):
        """Test sign up /post route w/ missing email data.""" 
        with app.test_client() as client:
            with app.app_context():
                data = {"first_name": "James", "last_name":"Kirk",
                "username": "chrome5x", "password":"jeff34523646", 
                "image_url": "https://cdn.vox-cdn.com/thumbor/Yt1avchDkHqEqJuhYZ3YjKF3kFc=/0x0:1700x960/1200x675/filters:focal(714x344:986x616)/cdn.vox-cdn.com/uploads/chorus_image/image/57514059/mario.0.jpg"}            
                res = client.post('/signup', data = data, follow_redirects=True)
                self.assertEqual(res.status_code, 400)
                
    def test_info_route(self):
        """Test sign up /post route w/ invalid password data.""" 
        with app.test_client() as client:
            with app.app_context():
                data = {"first_name": "James", "last_name":"Kirk",
                "username": "chrome5x", "email": "james@gmail.com", "password":"jef", 
                "image_url": "https://cdn.vox-cdn.com/thumbor/Yt1avchDkHqEqJuhYZ3YjKF3kFc=/0x0:1700x960/1200x675/filters:focal(714x344:986x616)/cdn.vox-cdn.com/uploads/chorus_image/image/57514059/mario.0.jpg"}             
                res = client.post('/signup', data = data, follow_redirects=True)
                self.assertEqual(res.status_code, 400)
                
    def test_info_route(self):
        """Test sign up /post route w/ missing password data.""" 
        with app.test_client() as client:
            with app.app_context():           
                data = {"first_name": "James", "last_name":"Kirk",
                "username": "chrome5x", "email": "james@gmail.com", "password":"jef", 
                "image_url": "https://cdn.vox-cdn.com/thumbor/Yt1avchDkHqEqJuhYZ3YjKF3kFc=/0x0:1700x960/1200x675/filters:focal(714x344:986x616)/cdn.vox-cdn.com/uploads/chorus_image/image/57514059/mario.0.jpg"}
                res = client.post('/signup', data = data, follow_redirects=True)
                self.assertEqual(res.status_code, 400)
                
class RandomizerTestCase_2(TestCase):
    """Integration tests (split into 2 classes) for flask app"""

    def setUp(self):
        db.drop_all()
        db.create_all()
        
        u1 = Users.signup("Jeffrey", "Johnson", "johnson@gmail.com")
        db.session.add(u1)
        db.session.flush()
        
        u2 = Users.signup("Marcy", "Rogers", "marcyrogers@outlook.com")
        db.session.add(u2)
        db.session.flush()
        
        from flask_bcrypt import Bcrypt
        bcrypt = Bcrypt()
        pass_hash_1 = bcrypt.generate_password_hash("pass_hash_1").decode('UTF-8')
        auth_u1 = Authentication("chrome2x", pass_hash_1, u1.user_id)
        db.session.add(auth_u1)
        db.session.flush()
        pass_hash_2 = bcrypt.generate_password_hash("pass_hash_2").decode('UTF-8')
        auth_u2 = Authentication("firefox2x", pass_hash_2, u2.user_id)
        db.session.add(auth_u2)
        db.session.flush()
        db.session.commit()
        self.u1 = u1
        self.u2 = u2
        self.u1.password = 'pass_hash_1'
        self.auth_u1 = auth_u1
        self.auth_u2 = auth_u2
        self.u2.password = 'pass_hash_2'
        
    def tearDown(self):
        db.drop_all()

    def test_randomizer_route(self):
        """Test randomizer route after login /get"""
        with app.test_client() as client:
            with app.app_context():
                with client.session_transaction() as change_session:
                    change_session['CURR_USER_KEY'] = self.u1.user_id
                res = client.get('/show')
                html = res.get_data(as_text=True)
                self.assertEqual(res.status_code, 200)
                self.assertIn('<h1>Filter Selections</h1>', html)
                

    def test_randomizer_route(self):
        """Test randomizer route after login valid (no missing data) /post (liking a movie)"""
        with app.test_client() as client:
            with app.app_context():
                with client.session_transaction() as change_session:
                    change_session['CURR_USER_KEY'] = self.u1.user_id
                data = {'like': 'True',
                        'name': "innerText",
                        'id': 54,
                        'type': 'Movies'}
                res = client.post('/show', data = data)
                html = res.get_data(as_text=True)
                self.assertEqual(res.status_code, 200)
                ##self.assertIn('<div class="tinder--cards" >', html)
                
    def test_randomizer_route(self):
        """Test randomizer route after login valid (no missing data) /post (liking a tv show)"""
        with app.test_client() as client:
            with app.app_context():
                with client.session_transaction() as change_session:
                    change_session['CURR_USER_KEY'] = self.u1.user_id
                data = {'like': 'True',
                        'name': "innerText",
                        'id': 54,
                        'type': 'TV_Show'}
                res = client.post('/show', data = data)
                html = res.get_data(as_text=True)
                self.assertNotIn('<div class="error" role="alert" id="messages">', html)            

##Think in order to get good test coverage of /show, I will need to test on the client side as the this page is making external API calls on the client-side rather than back-end
##This is then done through mock testing
                
    def test_randomizer_route(self):
        """Test randomizer route after login invalid /post"""
        with app.test_client() as client:
            with app.app_context():
                with client.session_transaction() as change_session:
                    change_session['CURR_USER_KEY'] = self.u1.user_id
                data = {'like': 'True',
                        'name': 'innerText',
                        'id': 54,
                         }
                res = client.post('/show', data = data)
                html = res.get_data(as_text=True)
                self.assertEqual(res.status_code, 400)
                self.assertIn('<div class="error" role="alert" id="messages">', html) 

    def login_route(self):
        """Test login route works /get"""
        with app.test_client() as client:
            with app.app_context():
                res = client.get('/login')
                self.assertEqual(res.status_code, 200)

    def login_route(self):
        """Test login route works /post"""
        with app.test_client() as client:
            with app.app_context():
                data = {'username': self.auth_u1, 'password': self.u1.password}
                res = client.post('/login', data = data)
                self.assertEqual(res.status_code, 302)

    def login_route(self):
        """Test login route works /post follow redirect"""
        with app.test_client() as client:
            with app.app_context():
                data = {'username': self.auth_u1, 'password': self.u1.password}
                res = client.post('/login', data = data, follow_redirects=True)
                self.assertEqual(res.status_code, 200)
                html = res.get_data(as_text=True)
                self.assertIn('<h5 class="mb-0">Friends</h5>', html)

    def logout(self):
        """Test logout route"""
        with app.test_client() as client:
            with app.app_context():
                with client.session_transaction() as change_session:
                    change_session['CURR_USER_KEY'] = self.u1.user_id
                res = client.get('/logout')
                self.assertEqual(res.status_code, 200)

    def edit_route(self):
        """Test edit route /get"""
        with app.test_client() as client:
            with app.app_context():
                with client.session_transaction() as change_session:
                    change_session['CURR_USER_KEY'] = self.u1.user_id
                res = client.get('/edit')
                self.assertEqual(res.status_code, 200)
                
    def edit_route(self):
        """Test edit route /post"""
        with app.test_client() as client:
            with app.app_context():
                with client.session_transaction() as change_session:
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
                res = client.post('/edit', data=data)
                self.assertEqual(res.status_code, 302)

    def edit_route(self):
        """Test edit route /post follow redirect"""
        with app.test_client() as client:
            with app.app_context():
                with client.session_transaction() as change_session:
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
                res = client.post('/edit', data=data, follow_redirects=True)
                self.assertEqual(res.status_code, 200)
                
    def edit_route(self):
        """Test edit route /post missing required data"""
        with app.test_client() as client:
            with app.app_context():
                with client.session_transaction() as change_session:
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
                res = client.post('/edit', data=data)
                html = res.get_data(as_text=True)
                self.assertIn('<div class="error" role="alert" id="messages">', html) 

    def edit_route(self):
        """Test edit route /post invalid email"""
        with app.test_client() as client:
            with app.app_context():
                with client.session_transaction() as change_session:
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
                res = client.post('/edit', data=data)
                html = res.get_data(as_text=True)
                self.assertIn('<div class="error" role="alert" id="messages">', html)


##Test randomizer (movies are added to queue in db)

    ##Possibly test JS (client-side code) with jest
    
##Test that queue actually shows in detail page



