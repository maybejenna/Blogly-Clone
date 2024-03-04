"""Seed file to make sample data for blogly db."""
from app import app
from datetime import datetime
from models import db, Users, Posts, Comment, Tag, PostTag

# Wrap database operations with app context
with app.app_context():
    # Drop all tables
    db.drop_all()
    # Create all tables
    db.create_all()

    # Clear existing data
    Users.query.delete()
    Posts.query.delete()
    Tag.query.delete()  # Clear existing tags

    # Add users
    user1 = Users(username='user1', first_name='First1', last_name='Last1')
    user2 = Users(username='user2', first_name='First2', last_name='Last2', img_url='images/user2img.png')
    user3 = Users(username='user3', first_name='First3', last_name='Last3')

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    # Add posts
    post1 = Posts(user_id=user1.id, title="Post 1 Title", content="Content of post 1", post_date=datetime(2024, 3, 1, 10, 0))
    post2 = Posts(user_id=user2.id, title="Post 2 Title", content="Content of post 2", post_date=datetime(2024, 3, 2, 11, 30))
    post3 = Posts(user_id=user3.id, title="Post 3 Title", content="Content of post 3", post_date=datetime(2024, 3, 3, 12, 45))

    db.session.add_all([post1, post2, post3])
    db.session.commit()

    # Add comments
    comment1 = Comment(content="Great post!", user_id=user1.id, post_id=post1.id, timestamp=datetime(2024, 3, 2, 13, 0))
    comment2 = Comment(content="Very informative!", user_id=user2.id, post_id=post1.id, timestamp=datetime(2024, 3, 2, 14, 15))
    comment3 = Comment(content="Nice work!", user_id=user3.id, post_id=post2.id, timestamp=datetime(2024, 3, 2, 16, 30))
    comment4 = Comment(content="I learned a lot!", user_id=user1.id, post_id=post3.id, timestamp=datetime(2024, 3, 3, 9, 45))
    comment5 = Comment(content="Thanks for sharing.", user_id=user2.id, post_id=post3.id, timestamp=datetime(2024, 3, 3, 11, 20))

    # Add new comment objects to session
    db.session.add_all([comment1, comment2, comment3, comment4, comment5])


    # Add tags
    tag1 = Tag(name="Fun")
    tag2 = Tag(name="Learning")
    tag3 = Tag(name="Challenging")

    db.session.add_all([tag1, tag2, tag3])
    db.session.commit()

    # Associate tags with posts
    # This assumes that the Posts model has a 'tags' relationship through the PostTag association table
    post1.tags.append(tag1)
    post1.tags.append(tag2)

    post2.tags.append(tag2)
    post2.tags.append(tag3)

    post3.tags.append(tag1)
    post3.tags.append(tag3)

    # Commit to save the associations
    db.session.commit()