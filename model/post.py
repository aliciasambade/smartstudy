from typing import Optional

import uuid
import datetime
from flask_login import LoginManager, UserMixin
import werkzeug.security as safe
import sirope
from werkzeug.security import generate_password_hash, check_password_hash


class Post:
    def __init__(self, img, title, time, user_id):
        self._post_id = str(uuid.uuid4())
        self._img = img
        self._title = title
        self._time = time
        self._user_id = user_id

    @property
    def post_id(self):
        return self._post_id

    @property
    def user_id(self):
        return self._user_id

    @property
    def img(self):
        return self._img

    @property
    def title(self):
        return self._title

    @property
    def time(self):
        return self._time

    @img.setter  # set img???
    def img(self, value):
        self._img = value

    @staticmethod
    def find(s: sirope.Sirope, post_id: str) -> "User":
        return s.find_first(Post, lambda p: p.post_id == post_id)

    def __str__(self):
        return f"Name: {self._post_id} {self._img} {self._title} {self._time}"

    # @staticmethod
    # def get_post_by_id(post_id):
    #     post_data = sirope.Sirope.load(Post, post_id)
    #     if post_data:
    #         return post_data[0]
    #     else:
    #         return None
