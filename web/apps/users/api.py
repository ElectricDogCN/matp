from flask import Blueprint, request, render_template, flash, redirect, url_for, get_flashed_messages, session, jsonify
from flask_login import login_required, login_user, logout_user, current_user

RESOURCE_NAME = "users"
resources_api = Blueprint(f'/{RESOURCE_NAME}_api_bp', __name__, url_prefix="/api/v1")


@resources_api.route(f'/login', methods=['get'], strict_slashes=False)
def get_resources():
    pass
