from web.exts import db
import sqlalchemy as sa


class Device(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    device_name = sa.Column(sa.String(64), nullable=False)
    device_info = sa.Column(sa.Text)
    owner_project = sa.Column(sa.Integer, nullable=False)
    is_root = sa.Column(sa.Boolean)
    status = sa.Column(sa.Boolean, nullable=False)
    activate = sa.Column(sa.Boolean, nullable=False)
    create_time = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now())
    modify_time = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
