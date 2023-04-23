from flask import Flask, Blueprint

from web.exts import db, login_manager, cors
from web import settings


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings.Config)

    db.init_app(app)
    login_manager.init_app(app)  # 初始化应用
    cors.init_app(app)

    from web.apps.users.views import user_views
    from web.apps.hosts.views import hosts_views
    app.register_blueprint(user_views)
    app.register_blueprint(hosts_views)

    from web.apps.hosts.api import resources_api as hosts_api
    from web.apps.users.api import resources_api as users_api
    from web.apps.devices.api import resources_api as devices_api
    from web.apps.historys.api import resources_api as historys_api
    from web.apps.projects.api import resources_api as projects_api
    from web.apps.scripts.api import resources_api as scripts_api
    from web.apps.sys.api import resources_api as sys_api
    from web.apps.tasks.api import resources_api as tasks_api
    from web.apps.api.api import resources_api as other_api
    app.register_blueprint(hosts_api)
    app.register_blueprint(users_api)
    app.register_blueprint(devices_api)
    app.register_blueprint(historys_api)
    app.register_blueprint(projects_api)
    app.register_blueprint(scripts_api)
    app.register_blueprint(sys_api)
    app.register_blueprint(tasks_api)
    app.register_blueprint(other_api)
    return app
