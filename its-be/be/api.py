from celery import shared_task
from flask import Blueprint, jsonify, redirect, render_template, request, url_for, abort
from flask_login import login_required, current_user
from pony.flask import db_session
import random
from datetime import date

from pony.orm import commit, flush

from .models import Course, Test, Question, UserAnswer
from .ml import generate_questions

import logging
logger = logging.getLogger(__name__)

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

@course_bp.route('/enroll', methods=['POST'])
@login_required
@db_session
def enroll_course():
    course = Course.get(id=request.json['course_id'])
    if course not in current_user.enrolled_courses:
        current_user.enrolled_courses.add(course)
        return jsonify(course.to_dict())
    abort(409)

 # /api/test
test_bp = Blueprint('test', __name__, url_prefix='/test')

@test_bp.route('/', methods=['GET'])
@login_required
@db_session
def get_tests():
    return jsonify([c.to_dict() for c in current_user.tests])

@test_bp.route('/generate', methods=['POST'])
@login_required
@db_session
def generate_test():
    course = Course.get(id=request.json['course_id'])
    if course not in current_user.enrolled_courses:
        abort(403)
    new_test = Test(for_user=current_user, course=course)
    commit()
    add_questions_to_test.delay(new_test.id)
    return jsonify(new_test.to_dict())

@shared_task()
@db_session
def add_questions_to_test(test_id):
    test = Test.get(id=test_id)
    user = test.for_user
    user_age = date.today().year - user.dob.year
    questions = Question.select().where(course=test.course)
    available_questions = []
    for q in questions:
        if test.for_user not in q.tests.for_user:
            age_range = q.age_range.split('-')
            if int(age_range[0]) <= user_age <= int(age_range[1]):
                available_questions.append(q)
    if len(available_questions) < 7:
        generate_result = generate_questions(test.course.name)
        for q in generate_result.questions:
            available_questions.append(Question(course=test.course, question=q.question, answer=q.answer, age_range=q.ageRange , difficulty=q.difficulty, explanation=q.explanation))
        commit()
    available_questions = random.sample(available_questions, 7)
    test.questions = available_questions
    test.ready = True

@test_bp.route('/<int:test_id>', methods=['GET', 'POST'])
@login_required
@db_session
def get_test(test_id):
    if request.method == 'POST':
        test = Test.get(id=test_id)
        if not test:
            abort(404)
        if current_user != test.for_user:
            abort(403)
        if test.completed or not test.ready:
            abort(409)
        user_answers = []
        for q in request.json['questions']:
            question = Question.get(id=q['id'])
            if not question:
                abort(404)
            if question not in test.questions:
                abort(403)
            user_answers.append(UserAnswer(test=test, question=question, answer=q['user_answer']))
        test.completed = True
        test.user_answers = user_answers
        return redirect(url_for('api.test.get_test', test_id=test_id))
    else:
        test = Test.get(id=test_id)
        if not test:
            abort(404)
        if current_user != test.for_user:
            abort(403)
        test_dict = test.to_dict()
        if not test.ready:
            return jsonify(test_dict)
        if test.completed:
            user_answers = [q for q in test.user_answers]
            user_answers_dict = []
            for a in user_answers:
                q_dict = a.question.to_dict()
                q_dict['user_answer'] = a.answer
                del q_dict['course']
                del q_dict['difficulty']
                user_answers_dict.append(q_dict)
            test_dict['questions'] = user_answers_dict
            return jsonify(test_dict)
        test_dict['questions'] = [q.to_dict() for q in test.questions]
        for q in test_dict['questions']:
            del q['answer']
            del q['explanation']
            del q['difficulty']
            del q['course']
        return jsonify(test_dict)

bp.register_blueprint(course_bp)
bp.register_blueprint(test_bp)
