# todo 添加host资源的restful api接口
from flask import Blueprint, request, render_template, flash, redirect, url_for, get_flashed_messages, session, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import update, delete

from web.apps.tasks.models import *

RESOURCE_NAME = "tasks"
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
    task = [class2dict(row) for row in db.session.scalars(db.select(Task).order_by(Task.create_time)).all()]
    if success:
        data = task
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
    task = db.session.scalars(db.select(Task).where(Task.id == res_id)).first()
    if task:
        data = class2dict(task)
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
    status = request.get_json().get('status')
    owner_project = request.get_json().get('owner_project')
    task = Task(status=status, owner_project=owner_project)
    db.session.add(task)
    db.session.commit()
    if task:
        data = class2dict(task)
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
    status = request.get_json().get('status')
    owner_project = request.get_json().get('owner_project')
    stmt = update(Task).where(Task.id == res_id).values(status=status, owner_project=owner_project)
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
    stmt = delete(Task).where(Task.id == res_id)
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


@resources_api.route(f'/{RESOURCE_NAME}/workflows', methods=['GET'], strict_slashes=False)
def get_workflows():
    body = RETURN_TEMPLATE.copy()
    success = True
    workflows = [class2dict(row) for row in db.session.scalars(db.select(Workflow).order_by(Workflow.id)).all()]
    if success:
        data = workflows
    else:
        data = None
        body.update(code=404)
        body.update(status="fail")
        body.update(message="未找到资源")
    body["data"] = data
    return body, body["code"]


@resources_api.route(f'/{RESOURCE_NAME}/workflows/<int:res_id>', methods=['GET'])
def get_workflow(res_id):
    body = RETURN_TEMPLATE.copy()
    success = True
    workflows = db.session.scalars(db.select(Workflow).where(Workflow.id == res_id)).first()
    if workflows:
        data = class2dict(workflows)
    else:
        data = None
        body.update(code=404)
        body.update(status="fail")
        body.update(message="未找到资源")
    body["data"] = data
    return body, body["code"]


@resources_api.route(f'/{RESOURCE_NAME}/workflows', methods=['POST'])
def post_workflows():
    success = True
    body = RETURN_TEMPLATE.copy()
    index = request.get_json().get('index')
    script_id = request.get_json().get('script_id')
    owner_task = request.get_json().get('owner_task')
    workflows = Workflow(index=index, owner_task=owner_task, script_id=script_id)
    db.session.add(workflows)
    db.session.commit()
    if workflows:
        data = class2dict(workflows)
    else:
        data = None
        body.update(code=404)
        body.update(status="fail")
        body.update(message="未找到资源")
    body["data"] = data
    return body, body["code"]


@resources_api.route(f'/{RESOURCE_NAME}/workflows/<int:res_id>', methods=['PUT'])
def put_workflows(res_id):
    body = RETURN_TEMPLATE.copy()
    success = True
    index = request.get_json().get('index')
    script_id = request.get_json().get('script_id')
    owner_task = request.get_json().get('owner_task')
    stmt = update(Workflow).where(Workflow.id == res_id).values(index=index, owner_task=owner_task, script_id=script_id)
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


@resources_api.route(f'/{RESOURCE_NAME}/workflows/<int:res_id>', methods=['DELETE'])
def delete_workflows(res_id):
    body = RETURN_TEMPLATE.copy()
    success = res_id
    stmt = delete(Workflow).where(Workflow.id == res_id)
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


@resources_api.route(f'/{RESOURCE_NAME}/run/<int:res_id>', methods=['GET'])
def run(res_id):
    body = RETURN_TEMPLATE.copy()
    success = res_id
    import os
    f = os.popen(r"C:\Users\asus\.conda\envs\matp_1\python.exe C:\Users\asus\Desktop\test.py")
    if success:
        data = f.readlines()
    else:
        data = None
        body.update(code=404)
        body.update(status="fail")
        body.update(message="未找到资源")
    f.close()
    body["data"] = data
    return body, body["code"]
