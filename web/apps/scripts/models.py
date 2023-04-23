from web.exts import db
import sqlalchemy as sa


class Script(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    script_name = sa.Column(sa.String(64), nullable=False)
    owner_project = sa.Column(sa.Integer, nullable=False)
    script_path = sa.Column(sa.Text, nullable=False)
    create_time = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now())
    modify_time = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
