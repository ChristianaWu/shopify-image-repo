import os
import unittest
 
from flask_image_repo import app, db
 
TEST_DB = 'test.db'
 
class BasicTests(unittest.TestCase):
 
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
     
    # executed after each test
    def tearDown(self):
        pass

    ########################
    #### helper methods ####
    ########################

    def signup(self, username, email, password):
        return self.app.post(
            '/signup',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def logout_user(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )


     
    ###############
    #### tests ####
    ###############
     
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_user_singup(self):
        self.register('bob','bob@gmail.com', 'bob')
        self.assertEqual(response.status_code, 200)

 
if __name__ == "__main__":
    unittest.main()