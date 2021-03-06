"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UsersViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()

    def test_add_message(self):
        """Can use add a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test
            
    
            resp = c.get(f'/users/{self.testuser.id}')
            self.assertEqual(resp.status_code, 200)

            resp = c.get('/users/999')
            self.assertEqual(resp.status_code, 404)

            resp = c.get(f'/users/{self.testuser.id}/following')
            self.assertEqual(resp.status_code, 200)

            resp = c.get('/users/999/following')
            self.assertEqual(resp.status_code, 404)

            resp = c.get(f'/users/{self.testuser.id}/followers')
            self.assertEqual(resp.status_code, 200)

            resp = c.get('/users/999/followers')
            self.assertEqual(resp.status_code, 404)




            next_user = User.signup(username="nexttestuser",
                                                email="nexttest@test.com",
                                                password="testuser",
                                                image_url=None)

            db.session.commit()

            resp = c.post(f'/users/follow/{next_user.id}')
            self.assertEqual(resp.status_code, 302)

            resp = c.post('/users/follow/9999')
            self.assertEqual(resp.status_code, 404)

            resp = c.post(f'/users/stop-following/{next_user.id}')
            self.assertEqual(resp.status_code, 302)

            resp = c.post('/users/stop-following/9999')
            self.assertEqual(resp.status_code, 404)

            resp = c.get('/users/profile')
            self.assertEqual(resp.status_code, 200)

            resp = c.post('/users/profile')
            self.assertEqual(resp.status_code, 200)

            resp = c.post('/users/delete')
            self.assertEqual(resp.status_code, 302)


            #unauthorized
                    #test all messages routes for unauthorized user
            resp = c.get('/logout')
            #messages_add

            # Make sure it redirects
            resp = c.get('/users')
            self.assertEqual(resp.status_code, 200)

            
            self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

            db.session.commit()


            resp = c.get(f'/users/{self.testuser.id}')
            self.assertEqual(resp.status_code, 200)

            resp = c.get(f'/users/{self.testuser.id}/following')
            self.assertEqual(resp.status_code, 302)

            resp = c.get(f'/users/{self.testuser.id}/followers')
            self.assertEqual(resp.status_code, 302)

            resp = c.post(f'/users/follow/{next_user.id}')
            self.assertEqual(resp.status_code, 302)

            resp = c.post(f'/users/stop-following/{next_user.id}')
            self.assertEqual(resp.status_code, 302)

            resp = c.get('/users/profile')
            self.assertEqual(resp.status_code, 302)

            resp = c.post('/users/delete')
            self.assertEqual(resp.status_code, 302)


