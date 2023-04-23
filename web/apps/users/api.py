from flask import Blueprint, request, render_template, flash, redirect, url_for, get_flashed_messages, session, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import update, delete
from web.apps.users.models import *

RESOURCE_NAME = "users"
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


@resources_api.route(f'/login', methods=['get'], strict_slashes=False)
def get_login():
    pass


@resources_api.route(f'/{RESOURCE_NAME}', methods=['GET'], strict_slashes=False)
def get_resources():
    body = RETURN_TEMPLATE.copy()
    success = True
    users = [class2dict(row) for row in db.session.scalars(db.select(User).order_by(User.id)).all()]
    if success:
        data = users
    else:
        data = None
        body.update(code=404)
        body.update(status="fail")
        body.update(message="未找到资源")
    body["data"] = data
    return body, body["code"]
