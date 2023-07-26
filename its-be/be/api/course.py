from flask import Blueprint, jsonify, redirect, request, url_for, abort
from flask_login import login_required, current_user
from pony.flask import db_session
from ..models import db

bp = Blueprint('course', __name__, url_prefix='/course')

@bp.route('/enrolled', methods=['GET'])
@login_required
@db_session
def get_courses():
    return jsonify([c.to_dict() for c in current_user.enrolled_courses])

@bp.route('/available', methods=['GET'])
@login_required
@db_session
def get_available_courses():
    all_courses = db.Course.select()
    enrolled_courses = current_user.enrolled_courses
    courses = [c.to_dict() for c in all_courses if c not in enrolled_courses]
    return jsonify(courses)
