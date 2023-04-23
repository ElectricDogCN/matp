from flask_login import UserMixin

from web.exts import db
import sqlalchemy as sa


class User(UserMixin, db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    username = sa.Column(sa.String(64), nullable=False)
    passwd = sa.Column(sa.String(64), nullable=False)

    def __init__(self, username, passwd) -> None:
        self.username = username
        self.passwd = passwd

    def check_passwd(self, passwd):
        return self.passwd == passwd
