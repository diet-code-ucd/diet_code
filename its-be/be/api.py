from flask import Blueprint, jsonify, redirect, render_template, request, url_for, abort
from flask_login import login_required, current_user
from pony.flask import db_session
import random

from be.models.tutor import UserAnswer

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
        questions = Question.select().filter(course=course)
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

def query_ml():
    pass

@test_bp.route('/<int:test_id>', methods=['GET', 'POST'])
@login_required
@db_session
def test(test_id):
    if request.method == 'POST':
        test = Test.get(id=test_id)
        if not test:
            abort(404)
        if current_user != test.for_user:
            abort(403)
        print(request.form)
        answers = []
        for q in test.questions:
            answers.append(UserAnswer(test=test, question=q, answer=request.form.get(str(q.id))))
        test.user_answers = answers
        score = 0
        for ua in answers:
            print(ua.question.answer + " == " + ua.answer + "?")
            if ua.question.answer == ua.answer:
                score += 1
        return jsonify({"score": score})
    else:
        test = Test.get(id=test_id)
        if not test:
            abort(404)
        if current_user != test.for_user:
            abort(403)
        return render_template('api/test.html', test=test)

bp.register_blueprint(course_bp)
bp.register_blueprint(test_bp)
