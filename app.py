import flask
import flask_login
import sirope
from model.user import User
from flask import render_template, redirect, request
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user


def create_app():
    login_manager = LoginManager()
    fapp = flask.Flask(__name__, instance_relative_config=True)
    sirp = sirope.Sirope()
    login_manager.init_app(fapp)

    return fapp, sirp, login_manager


app, srp, login_manager = create_app()

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

        login_user(user)
        return flask.render_template('home.html', user=user)
    return render_template('login.html')


@app.route('/home', methods=["GET", "POST"])
@login_required
def home():
    return render_template('home.html')


@app.route('/new_post', methods=["GET", "POST"])
@login_required
def new_post():
    if request.method == 'POST':

    return render_template('home.html')


@app.route('/logout')
@login_required
def logout():
    flask.session.clear()
    flask_login.logout_user()
    return redirect(url_for('/'))
