from flask import Blueprint, request, render_template, flash, redirect, url_for, get_flashed_messages, session
from flask_login import login_required, login_user, logout_user, current_user

hosts_views = Blueprint('hosts_views_bp', __name__, url_prefix="/hosts")


@hosts_views.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    data = {
        'title': 'Hello World',
        'name': 'Alice',
        'age': 25
    }
    return render_template("host/index.html", **data)
