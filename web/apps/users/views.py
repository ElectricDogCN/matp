from flask import Blueprint, request, render_template, flash, redirect, url_for, get_flashed_messages, session
from flask_login import login_required, login_user, logout_user, current_user

from web.apps.users.models import User, db
from web.exts import login_manager

user_views = Blueprint('user_views_bp', __name__)


@login_manager.user_loader
def load_user(user_id):
    user = db.get_or_404(User, user_id)
    return user


@user_views.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == "GET":
        return render_template('index.html', username=current_user.username)


@user_views.route('/register', methods=['GET', 'POST'])
def register():
    # 如果请求为post
    if request.method == 'POST':
        username = request.form.get('username')
        passwd = request.form.get('passwd')
        repasswd = request.form.get('repasswd')
        print(username, passwd)
        if passwd == repasswd:
            user = User(username, passwd)
            db.session.add(user)
            db.session.commit()
            return '注册成功'
        else:
            return '两次密码不一致'
    # 请求为get
    return render_template('register.html')


@user_views.route('/', methods=['GET', 'POST'])
@user_views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['passwd']
        print(passwd)
        if not username or not passwd:
            flash('Invalid input.')
            return redirect(url_for('user_views_bp.login'))
        user = User.query.filter_by(username=username).first()
        if not user:
            flash("用户不存在")
            return redirect(url_for('user_views_bp.login'))
        if username == user.username and user.check_passwd(passwd):
            login_user(user)  # 登入用户
            flash('Login success.')
            print("登录成功")
            return redirect(url_for('user_views_bp.index'))  # 重定向到主页

        flash('Invalid username or passwd.')  # 如果验证失败，显示错误消息
        return redirect(url_for('user_views_bp.login'))  # 重定向回登录页面
    if current_user.is_authenticated:
        return redirect(url_for('user_views_bp.index'))
    return render_template('login.html', msg=get_flashed_messages())


@user_views.route('/logout')  # 登出
@login_required
def logout():
    logout_user()
    session['_flashes'].clear()
    return redirect(url_for('user_views_bp.login'))
