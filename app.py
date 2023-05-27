import datetime

import flask
import flask_login
import sirope
import os
import redis

from PIL import Image
from model.user import User
from model.post import Post
from model.comment import Comment
from posts import posts
from users import users
from werkzeug.utils import secure_filename
from flask import render_template, redirect, request, session
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user
from flask import blueprints

# Definimos as respectivas rutas onde se van gardar as imaxes e os formatos permitidos
POSTS_FOLDER = os.path.join('static/images/posts')
COMMENTS_FOLDER = os.path.join('static/images/comments')
PROFILE_FOLDER = os.path.join('static/images/profile')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def create_app():
    login_manager = LoginManager()
    fapp = flask.Flask(__name__, instance_relative_config=True)
    sirp = sirope.Sirope()
    login_manager.init_app(fapp)
    fapp.register_blueprint(posts)
    fapp.register_blueprint(users)

    return fapp, sirp, login_manager


app, srp, lm = create_app()

# Engadimos á configuración o necesario
app.config['SECRET_KEY'] = 'clave'

app.config['POSTS_FOLDER'] = POSTS_FOLDER
app.config['COMMENTS_FOLDER'] = COMMENTS_FOLDER
app.config['PROFILE_FOLDER'] = PROFILE_FOLDER


@lm.user_loader
def load_user(email):
    return User.find(srp, email)


@app.route('/')
def index():
    return render_template('index.html')
