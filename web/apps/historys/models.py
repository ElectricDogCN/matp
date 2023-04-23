from web.exts import db
import sqlalchemy as sa


class History(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    owner_workflow = sa.Column(sa.Integer, nullable=False)
    executor_log = sa.Column(sa.Text)
    status = sa.Column(sa.Boolean)
    create_time = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now())
    end_time = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())


class Result(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    owner_workflow = sa.Column(sa.Integer, nullable=False)
    result_file_path = sa.Column(sa.Text, nullable=False)
    create_time = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now())
