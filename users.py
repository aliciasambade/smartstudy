import flask
import flask_login
import sirope
import os
from PIL import Image
from model.user import User
from model.post import Post
from model.comment import Comment
from werkzeug.utils import secure_filename
from flask import render_template, redirect, request, session, Blueprint, current_app
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user

users = Blueprint('users', __name__)

srp = sirope.Sirope()


@users.route('/sign_in', methods=["GET", "POST"])
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
            profile_img.save(os.path.join(current_app.config['PROFILE_FOLDER'], img))

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


@users.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['user_li']
        password = request.form['user_li_password']
        user = User.find(srp, email)
        if user and user.chk_password(password):
            login_user(user)
            return flask.redirect('/home')
        else:
            return flask.redirect('/')

    return flask.redirect('/')


@users.route('/logout')
@login_required
def logout():
    flask.session.clear()
    flask_login.logout_user()
    return redirect(url_for('/'))


def crop_image(img):
    crop = Image.open(img)
    width, height = crop.size
    size = min(width, height)
    left = (width - size) // 2
    top = (height - size) // 2
    right = (width + size) // 2
    bottom = (height + size) // 2

    return crop.crop((left, top, right, bottom))
