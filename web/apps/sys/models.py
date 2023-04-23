from web.exts import db
import sqlalchemy as sa


class Menu(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    tittle = sa.Column(sa.String(64), nullable=False)
    uri = sa.Column(sa.String(64))
    parent_id = sa.Column(sa.Integer, nullable=False)
    create_time = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now())
    modify_time = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())


class Permission(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer, nullable=False)
    menu_id = sa.Column(sa.Integer, nullable=False)
