"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""


    def setUp(self):
        """Create test client, add sample data."""
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers & no following & no likes
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(len(u.following), 0)
        self.assertEqual(len(u.likes), 0)

        # Make sure the intended attributes exist
        self.assertEqual(u.email, "test@test.com")
        self.assertEqual(u.username, "testuser")
        self.assertEqual(u.image_url, "/static/images/default-pic.png")
        self.assertEqual(u.header_image_url, "/static/images/warbler-hero.jpg")
        self.assertEqual(bool(u.bio), False)
        self.assertEqual(bool(u.location), False)
        self.assertEqual(u.password, "HASHED_PASSWORD")

        #Test the instance methods
        
        #Test the repr 
        self.assertEqual(u.__repr__(), f"<User #{u.id}: testuser, test@test.com>")
        
        
        
        #Test the class methods
         
        #Test signup
        new_user = User.signup('second_user', 'second@user.com', 'achooachoo', image_url = None)
        db.session.commit()
        self.assertEqual(new_user.username, 'second_user')
        
        #Test authenticate
        auth = User.authenticate('second_user', 'achooachoo')
        self.assertEqual((auth), new_user)

        auth = User.authenticate('second_user', 'wrongpassword')
        self.assertEqual((auth), False)

        auth = User.authenticate('notauser', 'achooachoo')
        self.assertEqual((auth), False)

        #Test is_followed_by
        result = new_user.is_followed_by(u)
        self.assertEqual(False, result)
        follow = Follows(user_being_followed_id=new_user.id, user_following_id= u.id)
        db.session.add(follow)
        db.session.commit()
        self.assertEqual(new_user.is_followed_by(u), True)

        #Test is_following
        self.assertEqual(new_user.is_following(u), False)
        self.assertEqual(u.is_following(new_user), True)
  


    