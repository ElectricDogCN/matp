from web.exts import db
import sqlalchemy as sa


class Host(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    ipaddr = sa.Column(sa.String(20), nullable=False)
    ssh_user = sa.Column(sa.String(64), nullable=False)
    ssh_passwd = sa.Column(sa.String(64), nullable=False)
    encoding = sa.Column(sa.String(16), nullable=False)
    status = sa.Column(sa.Boolean, nullable=False)
    activate = sa.Column(sa.Boolean, nullable=False)
    create_time = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now())
    modify_time = sa.Column(sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
