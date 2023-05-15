from typing import Optional

import uuid
import datetime
from flask_login import LoginManager, UserMixin
import werkzeug.security as safe
import sirope
from werkzeug.security import generate_password_hash, check_password_hash


class Post:
    def __init__(self, img, title, time):
        self._id = str(uuid.uuid4())
        self._img = img
        self._title = title
        self._time = time

    @property
    def img(self):
        return self._img

    @property
    def title(self):
        return self._title

    @property
    def time(self):
        return self._time

    @img.setter
    def img(self, value):
        self._img = value
