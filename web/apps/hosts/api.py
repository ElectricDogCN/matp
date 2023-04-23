# todo 添加host资源的restful api接口
from flask import Blueprint, request, render_template, flash, redirect, url_for, get_flashed_messages, session, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import update, delete

from web.apps.hosts.models import *

RESOURCE_NAME = "hosts"
resources_api = Blueprint(f'/{RESOURCE_NAME}_api_bp', __name__, url_prefix="/api/v1")

RETURN_TEMPLATE = {
    "code": 200,
    "status": "success",
    "message": '',
    "data": None
}


def class2dict(obj):
    # 创建一个空字典
    d = {}
    # 遍历对象的属性字典
    try:
        for k, v in obj.__dict__.items():
            # 如果属性名不是以双下划线开头和结尾的，就添加到字典中
            if not k.startswith('_') and not k.endswith('_'):
                d[k] = v
        # 返回字典
        return d
    except:
        return None


@resources_api.route(f'/{RESOURCE_NAME}', methods=['GET'], strict_slashes=False)
def get_resources():
    body = RETURN_TEMPLATE.copy()
    success = True
    hosts = [class2dict(row) for row in db.session.scalars(db.select(Host).order_by(Host.create_time)).all()]
    if success:
        data = hosts
    else:
        data = None
        body.update(code=404)
        body.update(status="fail")
        body.update(message="未找到资源")
    body["data"] = data
    return body, body["code"]


@resources_api.route(f'/{RESOURCE_NAME}/<int:res_id>', methods=['GET'])
def get_resource(res_id):
    body = RETURN_TEMPLATE.copy()
    success = True
    host = db.session.scalars(db.select(Host).where(Host.id == res_id)).first()
    if host:
        data = class2dict(host)
    else:
        data = None
        body.update(code=404)
        body.update(status="fail")
        body.update(message="未找到资源")
    body["data"] = data
    return body, body["code"]


@resources_api.route(f'/{RESOURCE_NAME}', methods=['POST'])
def post_resource():
    success = True
    body = RETURN_TEMPLATE.copy()
    ipaddr = request.form.get('ipaddr')
    ssh_user = request.form.get('ssh_user')
    ssh_passwd = request.form.get('ssh_passwd')
    encoding = request.form.get('encoding')
    status = bool(request.form.get('status'))
    activate = bool(request.form.get('activate'))
    host = Host(ipaddr=ipaddr, ssh_user=ssh_user, ssh_passwd=ssh_passwd, encoding=encoding, status=status,
                activate=activate)
    db.session.add(host)
    db.session.commit()
    if host:
        data = class2dict(host)
    else:
        data = None
        body.update(code=404)
        body.update(status="fail")
        body.update(message="未找到资源")
    body["data"] = data
    return body, body["code"]


@resources_api.route(f'/{RESOURCE_NAME}/<int:res_id>', methods=['PUT'])
def put_resource(res_id):
    body = RETURN_TEMPLATE.copy()
    success = True
    ipaddr = request.form.get('ipaddr')
    ssh_user = request.form.get('ssh_user')
    ssh_passwd = request.form.get('ssh_passwd')
    encoding = request.form.get('encoding')
    status = bool(request.form.get('status'))
    activate = bool(request.form.get('activate'))
    stmt = update(Host).where(Host.id == res_id).values(ipaddr=ipaddr, ssh_user=ssh_user, ssh_passwd=ssh_passwd,
                                                        encoding=encoding, status=status,
                                                        activate=activate)
    db.session.execute(stmt)
    db.session.commit()
    if success:
        data = {
            'title': 'Hello World',
            'name': 'Alice',
            'age': res_id
        }
    else:
        data = None
        body.update(code=404)
        body.update(status="fail")
        body.update(message="未找到资源")
    body["data"] = data
    return body, body["code"]


@resources_api.route(f'/{RESOURCE_NAME}/<int:res_id>', methods=['DELETE'])
def delete_resource(res_id):
    body = RETURN_TEMPLATE.copy()
    success = res_id
    stmt = delete(Host).where(Host.id == res_id)
    db.session.execute(stmt)
    db.session.commit()
    if success:
        data = {
            'title': 'Hello World',
            'name': 'Alice',
            'age': res_id
        }
    else:
        data = None
        body.update(code=404)
        body.update(status="fail")
        body.update(message="未找到资源")
    body["data"] = data
    return body, body["code"]
