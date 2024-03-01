"""Seed file to make sample data for blogly db."""

from app import app
from datetime import datetime
from models import db, Users, Posts

# Wrap database operations with app context
with app.app_context():
    # Drop all tables
    db.drop_all()
    # Create all tables
    db.create_all()

    # If table isn't empty, empty it
    User.query.delete()
    # Assuming you want to also clear out the posts
    Post.query.delete()

    # Add users
    user1 = User(username='user1', first_name='First1', last_name='Last1')
    user2 = User(username='user2', first_name='First2', last_name='Last2', img_url='images/user2img.png')
    user3 = User(username='user3', first_name='First3', last_name='Last3')

    # Add new user objects to session, so they'll persist
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)

    # Commit to save users because we need their IDs for the posts
    db.session.commit()

    # Add posts with explicit post_dates
    post1 = Posts(user_id=user1.id, title="Post 1 Title", content="Content of post 1", post_date=datetime(2024, 3, 1, 10, 0))
    post2 = Posts(user_id=user2.id, title="Post 2 Title", content="Content of post 2", post_date=datetime(2024, 3, 2, 11, 30))
    post3 = Posts(user_id=user3.id, title="Post 3 Title", content="Content of post 3", post_date=datetime(2024, 3, 3, 12, 45))

    # Add new post objects to session
    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)

    # Commit to save posts
    db.session.commit()