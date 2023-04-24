from flask import Blueprint, request, render_template, flash, redirect, url_for, get_flashed_messages, session, jsonify
from flask_login import login_required, login_user, logout_user, current_user

RESOURCE_NAME = "front"
resources_api = Blueprint(f'/{RESOURCE_NAME}_api_bp', __name__, url_prefix="/api/v1")


@resources_api.route(f'/login', methods=['POST'], strict_slashes=False)
def auth_resources():
    username = request.form.get('username')
    passwd = request.form.get('password')
    gen_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" \
                ".eyJ1aWQiOjUwMCwicmlkIjowLCJpYXQiOjE1MTI1NDQyOTksImV4cCI6MTUxMjYzMDY5OX0.eGrsrvwHm" \
                "-tPsO9r_pxHIQ5i5L1kX9RX444uwnRGaIM"
    return jsonify({
        "data": {
            "id": 500,
            "rid": 0,
            "username": username,
            "mobile": "123",
            "email": "123@qq.com",
            "token": "Bearer " + gen_token
        },
        "meta": {
            "msg": "登录成功",
            "status": 200
        }
    })


@resources_api.route(f'/menus', methods=['get'], strict_slashes=False)
def get_menus():
    return jsonify({
        'data': [
            {
                'id': 101,
                'authName': '用户管理',
                'path': 'null',
                'pid': 0,
                'children': [
                    {
                        'id': 104,
                        'authName': '商品列表',
                        'path': 'null',
                        'pid': 101,
                        'children': [
                            {
                                'id': 105,
                                'authName': '添加商品',
                                'path': 'null',
                                'pid': '104,101'
                            }
                        ]
                    }
                ]
            }
        ],
        'meta': {
            'msg': '获取权限列表成功',
            'status': 200
        }
    })
