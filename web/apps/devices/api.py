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
    device_name = request.get_json().get('device_name')
    owner_host = request.get_json().get('owner_host')
    device_info = request.get_json().get('device_info')
    status = request.get_json().get('status')
    activate = request.get_json().get('activate')

    device = Device(device_name=device_name, device_info=device_info, owner_host=owner_host, status=status,
                    activate=activate)
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
        data = [{"device_name": "device_name1", "device_info": """[hw_sc.build.os.apiversion]: [5]
[hw_sc.build.os.devicetype]: [phone]
[hw_sc.build.os.enable]: [true]
[hw_sc.build.os.releasetype]: [Release]
[hw_sc.build.os.version]: [2.1.0]
[hw_sc.build.platform.version]: [2.0.0]
[ro.bootimage.build.date]: [Thu Apr 21 11:53:50 CST 2022]
[ro.bootimage.build.date.utc]: [1590379237]
[ro.bootimage.build.fingerprint]: [Huawei/generic_a15/generic_a15:9/PPR1.180610.011/root202005251157:user/test-keys]
[ro.build.characteristics]: [default]
[ro.build.date]: [Thu Apr 21 11:51:40 CST 2022]
[ro.build.date.utc]: [1590379070]
[ro.build.description]: [MHA-AL00-user 102.0.0 HUAWEIMHA-AL00 150-CHN-LGRP1 release-keys]
[ro.build.display.id]: [MHA-AL00 9.1.0.228(C00E226R1P14)]
[ro.build.fingerprint]: [HUAWEI/MHA-AL00/HWMHA:9/HUAWEIMHA-AL00/9.1.0.228C00:user/release-keys]
[ro.build.hardware_expose]: [true]
[ro.build.hide]: [false]
[ro.build.hide.matchers]: [2.0.0]
[ro.build.hide.replacements]: [9.1.0]
[ro.build.hide.settings]: [8;1.8 GHz;2.0GB;11.00 GB;16.00 GB;1920 x 1080;9;4.9.148;9.1.0]
[ro.build.host]: [cn-west-3b-26fedf6211590377245358-7457cb54b-sszt8]
[ro.build.hw_emui_api_level]: [19]
[ro.build.id]: [HUAWEIMHA-AL00]
[ro.build.ohos.devicetype]: [phone]
[ro.build.preload_use_oemkey]: [true]
[ro.build.product]: [MHA]
[ro.build.soundrecorder.imgtag]: [true]
[ro.build.system_root_image]: [true]
[ro.build.tags]: [release-keys]
[ro.build.type]: [user]
[ro.build.update_version]: [V1_2]
[ro.build.user]: [test]
[ro.build.ver.physical]: [MHA-AL00 102.0.0.150(C00E150R1P3)]
[ro.build.version.all_codenames]: [REL]
[ro.build.version.base_os]: []
[ro.build.version.codename]: [REL]
[ro.build.version.emui]: [EmotionUI_9.1.0]
[ro.build.version.incremental]: [9.1.0.228C00]
[ro.build.version.min_supported_target_sdk]: [17]
[ro.build.version.preview_sdk]: [0]
[ro.build.version.release]: [9]
[ro.build.version.sdk]: [28]
[ro.build.version.security_patch]: [2020-05-01]
[ro.huawei.build.date]: [Thu Apr 21 11:51:40 CST 2022]
[ro.huawei.build.date.utc]: [1650513100]
[ro.huawei.build.display.id]: [MHA-AL00 2.0.0.150(C00E150R1P3)]
[ro.huawei.build.fingerprint]: [HUAWEI/MHA-AL00/HWMHA:9/HUAWEIMHA-AL00/102.0.0.150C00:user/release-keys]
[ro.huawei.build.host]: [cn-west-hcd-5a-2d58fcf021650510087841-76c777cd94-pw7xb]
[ro.huawei.build.version.incremental]: [102.0.0.150C00]
[ro.huawei.build.version.security_patch]: [2022-02-01]
[ro.odm.build.fingerprint]: [Huawei/Chicago/Chicago_MHA-AL00:9/PPR1.180610.011/20200522185648:user/release-keys]
[ro.vendor.build.date]: [Thu Apr 21 02:17:40 CST 2022]
[ro.vendor.build.date.utc]: [1590145153]
[ro.vendor.build.fingerprint]: [hi3660/hi3660/hi3660:9/PPR1.180610.011/root202005221856:user/release-keys]
[ro.vendor.build.security_patch]: [2018-06-19]""", "is_root": False},
                {"device_name": "device_name2", "device_info": "2", "is_root": False}]
    else:
        data = None
        body.update(code=404)
        body.update(status="fail")
        body.update(message="未找到资源")
    body["data"] = data
    return body, body["code"]
