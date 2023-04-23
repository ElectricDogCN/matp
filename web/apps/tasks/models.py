from web.exts import db
import sqlalchemy as sa


class Task(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    owner_project = sa.Column(sa.Integer, nullable=False)
    create_time = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now())
    status = sa.Column(sa.Boolean, nullable=False)


class Workflow(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    index = sa.Column(sa.Integer, nullable=False)
    owner_task = sa.Column(sa.Integer, nullable=False)
    script_id = sa.Column(sa.Integer, nullable=False)
    create_time = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now())
