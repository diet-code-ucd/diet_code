from flask import Blueprint, jsonify, redirect, request, url_for, abort
from flask_login import login_required, current_user
from pony.flask import db_session
import random

from .models import Course, Test, Question

bp = Blueprint('api', __name__, url_prefix='/api')

# /api/course
course_bp = Blueprint('course', __name__, url_prefix='/course')

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

@course_bp.route('/enroll', methods=['GET', 'POST'])
@login_required
@db_session
def enroll_course():
    if request.method == 'POST':
        course = Course.get(id=request.form['course_id'])
        if course not in current_user.enrolled_courses:
            current_user.enrolled_courses.add(course)
            return jsonify(course.to_dict())
        abort(409)
    return '''
        <form method="post">
            <p><input type=text name=course_id>
            <p><input type=submit value=Enroll>
        </form>
        '''

 # /api/test
test_bp = Blueprint('test', __name__, url_prefix='/test')

@test_bp.route('/', methods=['GET'])
@login_required
@db_session
def get_tests():
    return jsonify([c.to_dict() for c in current_user.tests])

@test_bp.route('/generate', methods=['GET', 'POST'])
@login_required
@db_session
def generate_test():
    if request.method == 'POST':
        course = Course.get(id=request.form['course_id'])
        if course not in current_user.enrolled_courses:
            abort(403)
        questions = Question.select().filter(course=1)
        available_questions = []
        for q in questions:
            if current_user not in q.tests.for_user:
                available_questions.append(q)
        available_questions = random.sample(available_questions, 7)
        new_test = Test(for_user=current_user, course=course, questions=available_questions)
        return jsonify(new_test.to_dict())
    return '''
        <form method="post">
            <p><input type=text name=course_id>
            <p><input type=submit value=Generate>
        </form>
    '''

bp.register_blueprint(course_bp)
bp.register_blueprint(test_bp)
