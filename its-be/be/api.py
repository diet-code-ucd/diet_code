from flask import Blueprint, jsonify, redirect, request, url_for, abort
from flask_login import login_required, current_user
from pony.flask import db_session

from .models import Course

bp = Blueprint('api', __name__, url_prefix='/api')
course_bp = Blueprint('course', __name__, url_prefix='/course')
test_bp = Blueprint('test', __name__, url_prefix='/test')

@course_bp.route('/enrolled', methods=['GET'])
@login_required
@db_session
def get_courses():
    return jsonify([c.to_dict() for c in current_user.enrolled_courses])

@course_bp.route('/available', methods=['GET'])
@login_required
@db_session
def get_available_courses():
    all_courses = Course.select()
    enrolled_courses = current_user.enrolled_courses
    courses = [c.to_dict() for c in all_courses if c not in enrolled_courses]
    return jsonify(courses)


@test_bp.route('/', methods=['GET'])
@login_required
@db_session
def get_tests():
    return jsonify([c.to_dict() for c in current_user.tests])

@test_bp.route('/generate', methods=['POST'])
@login_required
@db_session
def generate_test():
    course = Course.get(id=request.form['course_id'])
    if course not in current_user.enrolled_courses:
        abort(403)
    previous_test_questions = current_user.tests.select(lambda t: t.course == course).questions
    questions = course.test_questions.select(lambda q: q not in previous_test_questions)
    return jsonify([q.to_dict() for q in previous_test_questions])

bp.register_blueprint(course_bp)
bp.register_blueprint(test_bp)
