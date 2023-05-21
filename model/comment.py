import datetime
import uuid


class Comment:

    def __init__(self, comment, user_id, post_id):
        self._id = str(uuid.uuid4())
        self._comment = comment
        self._time = datetime.datetime.now()
        self._user_id = user_id
        self._post_id = post_id

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        self._comment = value

    @property
    def user_id(self):
        return self._user_id

    @property
    def post_id(self):
        return self._post_id

    def __str__(self):
        return f"Name: {self._comment}"
