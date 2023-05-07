from typing import Optional

from flask_login import LoginManager, UserMixin
import werkzeug.security as safe
import sirope
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin):
    def __init__(self, name, last_name, nickname, birth_date, phone_number, email, password):
        self._name = name
        self._last_name = last_name
        self._nickname = nickname
        self._birth_date = birth_date
        self._phone_number = phone_number
        self._email = email
        self._password = safe.generate_password_hash(password)
        self._posts_oids = []

    @property
    def name(self):
        return self._name

    @property
    def last_name(self):
        return self._last_name

    @property
    def nickname(self):
        return self._nickname

    @property
    def birth_date(self):
        return self._birth_date

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @property
    def oids_posts(self):
        if not self.__dict__.get("_posts_oids"):
            self._posts_oids = []
        return self._posts_oids

    def get_id(self):
        return self.email

    def chk_password(self, pswd):
        return safe.check_password_hash(self._password, pswd)

    def add_post_oid(self, post_oid):
        self.oids_posts.append(post_oid)

    @staticmethod
    def current_user():
        usr = flask_login.current_user

        if usr.is_anonymous:
            flask_login.logout_user()
            usr = None
        return usr

    @staticmethod
    def find(s: sirope.Sirope, email: str) -> "User":
        return s.find_first(User, lambda u: u.email == email)

    def __str__(self):
        return f"Name: {self._name} {self._last_name} {self._nickname} {self._email}"
