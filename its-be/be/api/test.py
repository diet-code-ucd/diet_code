from flask import Blueprint, jsonify, redirect, request, url_for, abort
from flask_login import login_required, current_user
from pony.flask import db_session

from be.models.tutor import Test
from ..models import db

bp = Blueprint('test', __name__, url_prefix='/test')

@bp.route('/', methods=['GET'])
@login_required
@db_session
def get_tests():
    user = db.User.get(username=current_user.username)
    return jsonify([c.to_dict() for c in user.tests])

@bp.route('/generate', methods=['POST'])
@login_required
@db_session
def generate_test():
    course = db.Course.get(id=request.form['course_id'])
    if course not in current_user.enrolled_courses:
        abort(403)
    previous_test_questions = current_user.tests.select(lambda t: t.course == course).questions
    questions = course.test_questions.select(lambda q: q not in previous_test_questions)
    return jsonify([q.to_dict() for q in previous_test_questions])
