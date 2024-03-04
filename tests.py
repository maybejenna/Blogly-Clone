# tests.py

import os
import unittest
from app import app, db
from models import connect_db, Users, Posts, Comment, Tag

class BloglyTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test client and seed sample data."""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        # Connect to the test database
        connect_db(app)
        
        # Create tables and add sample data
        db.drop_all()
        db.create_all()
        self.create_sample_data()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
    
    def create_sample_data(self):
        """Create sample data for testing."""
        # Add sample data
        user = Users(username='testuser', first_name='Test', last_name='User')
        post = Posts(user_id=1, title="Test Post", content="Content for test post")
        tag = Tag(name="TestTag")
        
        db.session.add_all([user, post, tag])
        db.session.commit()

    def test_home_page(self):
        """Test the home page route."""
        with app.app_context():
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Posts', response.data)

    def test_new_user(self):
        """Test the new user creation route."""
        with app.app_context():
            response = self.client.post('/users/new', data={
                'username': 'newuser',
                'first_name': 'New',
                'last_name': 'User'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'New User', response.data)


if __name__ == '__main__':
    unittest.main()