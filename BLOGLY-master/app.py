"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'imsocool'

app.debug = False
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def redirect_to_users():
    """ Redirects to the list of users. """

    return redirect('/users')


@app.route('/users')
def show_index():
    """ Show all users list and link to add-user """
    
    users = User.query.all()
    
    return render_template('users_list.html', users=users)


@app.route('/users/new')
def show_create_page():
    """ Show the new user creation form """

    return render_template('user_form.html')


@app.route('/users/new', methods=["POST"])
def handle_new_user():
    """ Obtain Form info and place into database """

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:id>')
def show_user_profile(id):
    """ Return the user's profile page """
    
    user = User.query.get(id)
    return render_template('user_profile.html', user=user)


@app.route('/users/<int:id>/edit')
def show_edit_page(id):
    """ Display the edit page for selected user """

    return render_template('edit_page.html', id=id)

@app.route('/users/<int:id>/edit', methods=["POST"])
def handle_edit(id):
    """ Obtain Form info and update the database """
    user = User.query.get(id)
    
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:id>/delete', methods=["POST"])
def delete_user(id):
    """ Delete the user by id from the database and redirect
        to the users list """

    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

# POST ROUTES

@app.route('/users/<int:id>/posts/new') 
def show_post_form(id):
    """ Show the post form """

    user = User.query.get(id)

    return render_template('post_form.html', user=user, user_id=id)

@app.route('/users/<int:id>/posts/new', methods=["POST"])
def handle_post_form(id):
    """ Handle the form data to append into Posts table 
        and redirect to the user's profile """

    post_title = request.form['title']
    post_content = request.form['content']

    new_post = Post(title=post_title, 
                    content=post_content,
                    user_id=id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """ Show the post """

    post = Post.query.get(post_id)

    return render_template('post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """ Show the edit form """

    post = Post.query.get(post_id)
    
    return render_template('post_edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_post_edit(post_id):
    """ Handle the post edit form and update the Posts table """

    post = Post.query.get(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """ Delete the post from the Posts table """

    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect('/users')
