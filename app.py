import datetime

import flask
import flask_login
import sirope
import os
from model.user import User
from model.post import Post
from werkzeug.utils import secure_filename
from flask import render_template, redirect, request
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user

UPLOAD_FOLDER = os.path.join('static/images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def create_app():
    login_manager = LoginManager()
    fapp = flask.Flask(__name__, instance_relative_config=True)
    sirp = sirope.Sirope()
    login_manager.init_app(fapp)

    return fapp, sirp, login_manager


app, srp, login_manager = create_app()

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'clave'


@login_manager.user_loader
def load_user(email):
    return User.find(srp, email)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sign_in', methods=["GET", "POST"])
def sign_in():
    if request.method == 'POST':
        name = request.form['user_name']
        surname = request.form['user_surname']
        nickname = request.form['user_nickname']
        birthday = request.form['user_birthday']
        phonenumber = request.form['user_phonenumber']
        email = request.form['user_email']
        password = request.form['user_password']
        user = User(name, surname, nickname, birthday, phonenumber, email, password)
        print(user)
        srp.save(User(name, surname, nickname, birthday, phonenumber, email, password))
        users = list(srp.load_last(User, 10))
        sust = {
            "users_list": users,
            "user": current_user
        }
        login_user(user)

        return flask.render_template('home.html', **sust)
    return render_template('sign_in.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['user_li']
        password = request.form['user_li_password']
        user = User.find(srp, email)

        posts = list(srp.load_last(Post, 10))
        print("ola esto é post login")
        sust = {
            "posts": posts,
            "user": current_user
        }
        print("este esta enriba do primeiro return")
        return flask.redirect('/home')

    print("este esta enriba do segundo return")
    return render_template('login.html')


@app.route('/home', methods=["GET", "POST"])
@login_required
def home():
    if request.method == 'POST':
        # img = request.files['post_photo'].read()
        photo = request.files['post_photo']
        title = request.form['post_title']
        time = datetime.datetime.now()
        # ruta = "images/test.jpg"
        # with open(ruta, "ab") as f:
        #    f.write(img)
        # srp.save(Post(ruta, title, time))
        img = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], img))
        srp.save(Post(img, title, time))
        posts = list(srp.load_last(Post, 10))

        users = list(srp.load_last(User, 10))
        sust = {
            "posts": posts,
            "user": current_user,
            "users_list": users
        }
        return flask.render_template('home.html', **sust)

    posts = list(srp.load_last(Post, 10))
    print("ola esto é post login")
    sust = {
        "posts": posts,
        "user": current_user
    }
    return flask.render_template('home.html', **sust)


@app.route('/logout')
@login_required
def logout():
    flask.session.clear()
    flask_login.logout_user()
    return redirect(url_for('/'))


def get_posts():
    posts = list(srp.load_all(Post))
    return posts
