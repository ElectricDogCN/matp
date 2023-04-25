# todo 添加host资源的restful api接口
from flask import Blueprint, request, render_template, flash, redirect, url_for, get_flashed_messages, session, jsonify, \
    send_file
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import update, delete

from web.apps.scripts.models import *

RESOURCE_NAME = "scripts"
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
    project_id = request.args.get('query')
    script = [class2dict(row) for row in db.session.scalars(
        db.select(Script).where(Script.owner_project == project_id).order_by(Script.create_time)).all()]
    if success:
        data = script
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
    script = db.session.scalars(db.select(Script).where(Script.id == res_id)).first()
    if script:
        data = class2dict(script)
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
    script_name = request.get_json().get('script_name')
    owner_project = request.get_json().get('owner_project')
    script_path = request.get_json().get('script_path')
    script = Script(script_name=script_name, owner_project=owner_project, script_path=script_path)
    db.session.add(script)
    db.session.commit()
    if script:
        data = class2dict(script)
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
    script_name = request.get_json().get('script_name')
    owner_project = request.get_json().get('owner_project')
    script_path = request.get_json().get('script_path')
    stmt = update(Script).where(Script.id == res_id).values(script_name=script_name, owner_project=owner_project,
                                                            script_path=script_path)
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
    stmt = delete(Script).where(Script.id == res_id)
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


@resources_api.route(f'/{RESOURCE_NAME}/upload', methods=['POST'])
def upload():
    file = request.files.get('file')  # 获取上传的文件对象
    if file:
        filename = file.filename  # 获取文件名
        file.save(r'C:\Users\asus\PycharmProjects\github\matp\web\upload\scripts\\' + filename)  # 保存文件到upload目录下
    body = RETURN_TEMPLATE.copy()
    success = file
    if success:
        data = r'C:\Users\asus\PycharmProjects\github\matp\web\upload\scripts\\' + filename
    else:
        data = None
        body.update(code=404)
        body.update(status="fail")
        body.update(message="未找到资源")
    body["data"] = data
    return body, body["code"]


@resources_api.route(f'/{RESOURCE_NAME}/download/<string:filename>', methods=['GET'])
def download(filename):
    return send_file('./upload/scripts/' + filename)
