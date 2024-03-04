"""Blogly application."""

from flask import Flask, request, redirect, render_template, url_for
from models import db, connect_db, Users, Posts, Comment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

# Wrap the db.create_all() call with app.app_context()
with app.app_context():
    db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/users")
def list_users():
    """List users and show add form."""

    users = Users.query.all()
    return render_template("list.html", users=users)

@app.route("/users/new", methods=["GET", "POST"])
def new_user():
    """Show form for adding a new user and process the form."""
    if request.method == "POST":
        # Extract form data
        username = request.form.get("username")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        img_url = request.form.get("img_url") or None  # Use default if empty

        # Create a new Users instance
        new_user = Users(username=username, first_name=first_name, last_name=last_name, img_url=img_url)

        # Add to database and commit
        db.session.add(new_user)
        db.session.commit()

        # Redirect to the new user's page, using the ID of the newly created user
        return redirect(url_for("show_individual_user", user_id=new_user.id))

    # For GET request, just show the form
    return render_template("new_user.html")

@app.route("/users/<int:user_id>")
def show_individual_user(user_id):
    """Show details for a single user."""
    user = Users.query.get_or_404(user_id)
    return render_template("individual_user.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["GET"])
def show_edit_page(user_id):
    """Show the edit page for a user."""
    user = Users.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Process the edit form, updating the user."""
    user = Users.query.get_or_404(user_id)
    user.username = request.form['username']
    user.first_name = request.form['first_name']
    user.last_name = request.form.get('last_name')  # Using .get() as last_name might be empty
    user.img_url = request.form.get('img_url', user.img_url)  # Default to existing if not provided

    db.session.commit()
    return redirect(url_for('list_users'))

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete the user."""
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_users'))


@app.route("/posts/new", methods=["GET", "POST"])
def add_post(user_id):
    """Show form to add a post for that user and handle the form submission."""
    user = Users.query.get_or_404(user_id)

    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        new_post = Posts(title=title, content=content, user_id=user.id)

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('show_individual_user', user_id=user.id))
    
    return render_template("add_post.html", user=user)

@app.route('/posts')
def show_posts():
    # Query for all posts
    posts = Posts.query.all()
    # Render an HTML template, passing the posts
    return render_template('posts.html', posts=posts)


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show details for a single post."""
    post = Posts.query.get_or_404(post_id)
    return render_template("post_detail.html", post=post)


