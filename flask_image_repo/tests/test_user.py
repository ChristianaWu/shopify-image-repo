# project/test_users.py


import os
import unittest

from project import app, db
from project.models import Seller


TEST_DB = 'user.db'


class UsersTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        mail.init_app(app)
        self.assertEquals(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass


    ########################
    #### helper methods ####
    ########################

    def register(self, username, email, password):
        return self.app.post(
            '/register',
            data=dict(username=username, email=email, password=password),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )


    ###############
    #### tests ####
    ###############


    def test_valid_user_singup(self):
        response = self.signup('bob', 'bob@gmail.com', 'password')
        self.assertEqual(response.status_code, 200)
        assert request.path == url_for('home')

    def test_duplicate_email_user_registration_error(self):
        self.app.get('/signup', follow_redirects=True)
        self.signup('bob', 'bob@gmail.com', 'password')
        self.app.get('/register', follow_redirects=True)
        response = self.signup('bob', 'bob@gmail.com', 'password')
        self.assertIn(b'This email already has an account.', response.data)

    def test_missing_field_user_registration_error(self):
        self.app.get('/signup', follow_redirects=True)
        response = self.register('jon@gmail.com', '')
        self.assertIn(b'Please fill out this field.', response.data)

    def test_login_form_displays(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_valid_login(self):
        self.app.get('/signup', follow_redirects=True)
        self.register('bob','bob@gmail.com', 'bob')
        self.app.get('/login', follow_redirects=True)
        response = self.login('bob@gmail.com', 'bob')
        self.assertEqual(response.status_code, 200)

    def test_login_without_registering(self):
        self.app.get('/login', follow_redirects=True)
        response = self.login('admin@gmail.com', 'admin')
        self.assertIn(b'Password or Email is incorrect try again!', response.data)

    def test_valid_logout(self):
        self.app.get('/signup', follow_redirects=True)
        self.register('bob','bob@gmail.com', 'bob')
        self.app.get('/login', follow_redirects=True)
        self.login('bob@gmail.com', 'bob')
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_user_profile_page(self):
        self.app.get('/signup', follow_redirects=True)
        self.register('bob','bob@gmail.com', 'bob')
        self.app.get('/login', follow_redirects=True)
        self.login('bob@gmail.com', 'bob')
        response = self.app.get('/account', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'bob', response.data)
        self.assertIn(b'bob@gmail.com', response.data)


if __name__ == "__main__":
    unittest.main()
