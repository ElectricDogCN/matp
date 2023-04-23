from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://matp:123456+Matp@rm-cn-5yd36a8mv0014hlo.rwlb.rds.aliyuncs.com:3306/matp'

db = SQLAlchemy()
login_manager = LoginManager()  # 实例化登录管理对象
login_manager.login_view = 'user_views_bp.login'
cors = CORS()
