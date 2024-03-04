"""Models for Blogly."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class Users(db.Model):
    """Users."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    username = db.Column(db.String(50),
                         nullable=False,
                         unique=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(30), nullable=True)
    img_url = db.Column(db.String, default="images/default_user_img.png")


    posts = db.relationship('Posts', backref='user', lazy=True, cascade="all, delete-orphan")
    comments = db.relationship('Comment', back_populates='user')

    def __repr__(self):
        """Show info about user."""
        return f"<User {self.id} {self.username} {self.first_name} {self.last_name}>"
    

class Posts(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)  # Assuming you want a title for posts
    content = db.Column(db.String(), nullable=False)
    post_date = db.Column(db.DateTime, server_default=db.func.now())

    comments = db.relationship('Comment', back_populates='post', cascade="all, delete-orphan")

    def __repr__(self):
        """Show info about post."""
        return f"<Post {self.id} {self.title}>"
    
class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    user = db.relationship('Users', back_populates='comments')
    post = db.relationship('Posts', back_populates='comments')