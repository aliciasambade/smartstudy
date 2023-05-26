import datetime

import flask
import flask_login
import sirope
import os
from PIL import Image
from model.user import User
from model.post import Post
from model.comment import Comment

from werkzeug.utils import secure_filename
from flask import render_template, redirect, request, session
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user

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


def validate_password(password):
    while True:
        if len(password) < 8:
            print("Asegúrate de que tu contraseña tenga al menos 8 caracteres")
        elif re.search('[0-9]', password) is None:
            print("Asegúrate de que tu contraseña tenga un número")
        elif re.search('[A-Z]', password) is None:
            print("Asegúrate de que tu contraseña tenga una letra mayúscula")
        else:
            print("Tu contraseña parece correcta")
            break


def nickname_exists(nickname):
    users = srp.load_all(User)
    for user in users:
        if user.nickname == nickname:
            return True
    return False


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

        profile_img = request.files['profile_photo']
        if profile_img is None or profile_img.filename == '':
            img = 'profile_photo.png'
        else:
            img = secure_filename(profile_img.filename)
            print(img)
            profile_img = crop_image(profile_img)
            profile_img.save(os.path.join(app.config['PROFILE_FOLDER'], img))

        user = User(name, surname, nickname, birthday, phonenumber, email, password, img)
        print(user)
        srp.save(User(name, surname, nickname, birthday, phonenumber, email, password, img))
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
        login_user(user)
        return flask.redirect('/home')
    return flask.redirect('/')


@app.route('/home', methods=["GET", "POST"])
@login_required
def home():
    if request.method == 'POST':
        photo = request.files['post_photo']
        title = request.form['post_title']
        time = datetime.datetime.now()
        img = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['POSTS_FOLDER'], img))
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
@app.route('/view_post/<post_id>', methods=['GET', 'POST'])
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
            "users": users,
            "user": current_user
        }
        return render_template('view_post.html', **sust)
    comments = list(srp.load_last(Comment, 10))
    sust = {
        "post": post,
        "comments": comments,
        "user": current_user
    }
    return render_template('view_post.html', **sust)


@app.route('/logout')
@login_required
def logout():
    flask.session.clear()
    flask_login.logout_user()
    return redirect(url_for('/'))


def get_posts():
    posts = list(srp.load_all(Post))
    return posts


def crop_image(img):
    crop = Image.open(img)
    width, height = crop.size
    size = min(width, height)
    left = (width - size) // 2
    top = (height - size) // 2
    right = (width + size) // 2
    bottom = (height + size) // 2

    return crop.crop((left, top, right, bottom))
