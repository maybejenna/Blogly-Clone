"""Blogly application."""

from flask import Flask, request, redirect, render_template, url_for, flash
from models import db, connect_db, Users, Posts, Comment, Tag, PostTag

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
    
    recent_posts = Posts.query.order_by(Posts.post_date.desc()).limit(5).all()
    return render_template("home.html", recent_posts=recent_posts)

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
    user = Users.query.get_or_404(user_id)
    recent_posts = Posts.query.filter_by(user_id=user_id).order_by(Posts.post_date.desc()).limit(3).all()
    return render_template("individual_user.html", user=user, recent_posts=recent_posts)


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

@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
def show_add_post_form(user_id):
    """Show form to add a post for that user."""
    user = Users.query.get_or_404(user_id)
    return render_template("add_post.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    title = request.form['title']
    content = request.form['content']
    # If using hidden input for user_id, you can directly use the user_id parameter from the route.
    new_post = Posts(title=title, content=content, user_id=user_id)
    selected_tags = request.form.getlist('tags') 
    new_post.tags = [Tag.query.get(tag_id) for tag_id in selected_tags]

    db.session.add(new_post)
    db.session.commit()

    flash('New post added successfully!', 'success')
    return redirect(url_for("show_individual_user", user_id=user_id))

@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def show_edit_post_form(post_id):
    post = Posts.query.get_or_404(post_id)
    return render_template('edit_post_form.html', post=post)

# Route to handle the form submission
@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    post = Posts.query.get_or_404(post_id)
    post.title = request.form.get('title')
    post.content = request.form.get('content')
    selected_tags = request.form.getlist('tags')  # Assuming 'tags' is the name of your input field for tags
    new_post.tags = [Tag.query.get(tag_id) for tag_id in selected_tags]
    db.session.commit()
    db.session.commit()
    return redirect(url_for('show_post', post_id=post_id))

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete the post."""
    post = Posts.query.get_or_404(user_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('list_users'))

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route("/tags")
def list_tags():
    tags = Tag.query.all()
    return render_template("list_tags.html", tags=tags)

@app.route("/tags/<int:tag_id>")
def tag_detail(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag_detail.html", tag=tag)

@app.route('/posts/<int:post_id>/add_tag', methods=['POST'])
def add_tag_to_post(post_id):
    post = Posts.query.get_or_404(post_id)
    new_tag_name = request.form['new_tag_name']
    db.session.commit()
    flash('New tag added successfully!', 'success')
    return redirect(url_for('show_post', post_id=post_id))

@app.route("/tags/new", methods=["GET", "POST"])
def new_tag():
    if request.method == "POST":
        name = request.form["name"]
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for("list_tags"))
    return render_template("new_tag.html")

@app.route("/tags/<int:tag_id>/edit", methods=["GET", "POST"])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    if request.method == "POST":
        tag.name = request.form["name"]
        db.session.commit()
        return redirect(url_for("list_tags"))
    return render_template("edit_tag.html", tag=tag)

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for("list_tags"))