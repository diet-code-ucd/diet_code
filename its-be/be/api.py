import json
from flask import Blueprint, redirect, request, url_for, abort
from flask_login import login_required, current_user
from .models import db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/courses', methods=['GET'])
@login_required
def get_courses():
    user = db.User.get(username=current_user.username)
    return json.dumps([c.to_dict() for c in user.enrolled_courses])

@bp.route('/tests', methods=['GET'])
@login_required
def get_courses():
    user = db.User.get(username=current_user.username)
    return json.dumps([c.to_dict() for c in user.tests])
