import os

from flask import send_from_directory, jsonify
from flask_migrate import Migrate
from web.exts import db
from web.apps.users.models import User
from web.apps.hosts.models import Host
from web.apps.devices.models import Device
from web.apps.historys.models import History, Result
from web.apps.hosts.models import Host
from web.apps.projects.models import Project
from web.apps.scripts.models import Script
from web.apps.sys.models import Menu, Permission
from web.apps.tasks.models import Task, Workflow

from web.apps import create_app

app = create_app()
migrate = Migrate(app=app, db=db)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),  # 对于当前文件所在路径,比如这里是static下的favicon.ico
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/test')
def test():
    data = {"test1": ["test11", "test12", "test13", ], "test2": "tset21"}
    return jsonify(data)


if __name__ == '__main__':
    print(app.url_map)
    app.run()
