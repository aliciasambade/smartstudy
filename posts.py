import flask
import flask_login
import sirope
import os
import datetime
from PIL import Image
from model.user import User
from model.post import Post
from model.comment import Comment
from werkzeug.utils import secure_filename
from flask import render_template, redirect, request, session, Blueprint, current_app
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user

posts = Blueprint('posts', __name__)

srp = sirope.Sirope()


@posts.route('/home', methods=["GET", "POST"])
@login_required
def home():
    if request.method == 'POST':
        photo = request.files['post_photo']
        title = request.form['post_title']
        time = datetime.datetime.now()
        img = secure_filename(photo.filename)
        photo.save(os.path.join(current_app.config['POSTS_FOLDER'], img))
        user = current_user
        user_id = user._user_id
        print(user_id)
        srp.save(Post(img, title, time, user_id))
        print(user.__dict__)

    posts = list(srp.load_all(Post))
    users = list(srp.load_all(User))
    sust = {
        "posts": posts,
        "user": current_user,
        "users": users
    }
    return flask.render_template('home.html', **sust)


@login_required
@posts.route('/view_post/<post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    post = Post.find(srp, post_id)
    if request.method == 'POST':
        comment = request.form['commentText']
        srp.save(Comment(comment, current_user._user_id, post_id))

    users = list(srp.load_all(User))
    comments = list(srp.load_last(Comment, 10))
    sust = {
        "post": post,
        "comments": comments,
        "user": current_user,
        "users": users,
    }
    return render_template('view_post.html', **sust)
