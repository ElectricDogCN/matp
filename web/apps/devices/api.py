# todo 添加host资源的restful api接口
from flask import Blueprint, request, render_template, flash, redirect, url_for, get_flashed_messages, session, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import update, delete

from web.apps.devices.models import *

RESOURCE_NAME = "devices"
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
    for k, v in obj.__dict__.items():
        # 如果属性名不是以双下划线开头和结尾的，就添加到字典中
        if not k.startswith('_') and not k.endswith('_'):
            d[k] = v
    # 返回字典
    return d


@resources_api.route(f'/{RESOURCE_NAME}', methods=['GET'], strict_slashes=False)
def get_resources():
    body = RETURN_TEMPLATE.copy()
    success = True
    devices = [class2dict(row) for row in db.session.scalars(db.select(Device).order_by(Device.device_name)).all()]
    devices = devices
    if success:
        data = devices
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
    devices = [class2dict(row) for row in db.session.scalars(db.select(Device).where(Device.id == res_id)).all()]
    devices = devices
    if success:
        data = devices
    else:
        data = None
        body.update(code=404)
        body.update(status="fail")
        body.update(message="未找到资源")
    body["data"] = data
    return body, body["code"]


@resources_api.route(f'/{RESOURCE_NAME}', methods=['POST'])
def post_resource():
    body = RETURN_TEMPLATE.copy()
    success = True
    device_name = request.form.get('device_name')
    owner_host = request.form.get('owner_host')
    status = request.form.get('status')
    activate = request.form.get('activate')

    device = Device(device_name=device_name, owner_host=owner_host, status=status, activate=activate)
    db.session.add(device)
    db.session.commit()
    if device:
        data = class2dict(device)
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
    success = res_id
    device_name = request.form.get('device_name')
    owner_host = request.form.get('owner_host')
    status = request.form.get('status')
    activate = request.form.get('activate')
    stmt = update(Device).where(Device.id == res_id).values(device_name=device_name, owner_host=owner_host,
                                                            status=status, activate=activate)
    db.session.execute(stmt)
    db.session.commit()
    if success:
        data = {"id": res_id}
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
    stmt = delete(Device).where(Device.id == res_id)
    db.session.execute(stmt)
    db.session.commit()
    if success:
        data = {"id": res_id}
    else:
        data = None
        body.update(code=404)
        body.update(status="fail")
        body.update(message="未找到资源")
    body["data"] = data
    return body, body["code"]


@resources_api.route(f'/{RESOURCE_NAME}/instances/<int:res_id>', methods=['GET'])
def get_devices_instance(res_id):
    body = RETURN_TEMPLATE.copy()
    success = res_id

    if success:
        data = [{"device_name": "device_name1", "device_info": "1", "is_root": False},
                {"device_name": "device_name2", "device_info": "2", "is_root": False}]
    else:
        data = None
        body.update(code=404)
        body.update(status="fail")
        body.update(message="未找到资源")
    body["data"] = data
    return body, body["code"]
