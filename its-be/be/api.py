from celery import shared_task
from flask import Blueprint, jsonify, redirect, render_template, request, url_for, abort
from flask_login import login_required, current_user
from pony.flask import db_session
import random

from pony.orm import commit, flush

from .models import Course, Test, Question, UserAnswer
from .ml import generate_questions

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
    #TODO: Actually make this async
    add_questions_to_test.delay(new_test.id)
    return jsonify(new_test.to_dict())

@shared_task()
@db_session
def add_questions_to_test(test_id):
    test = Test.get(id=test_id)
    questions = Question.select().filter(course=test.course)
    available_questions = []
    for q in questions:
        if test.for_user not in q.tests.for_user:
            available_questions.append(q)
    if len(available_questions) < 7:
        generate_result = generate_questions(test.course.name)
        for q in generate_result.questions:
            available_questions.append(Question(course=test.course, question=q.question, answer=q.answer, difficulty=q.difficulty, explanation=q.explanation))
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
        for q in request.json['questions']:
            question = Question.get(id=q['id'])
            if not question:
                abort(404)
            if question not in test.questions:
                abort(403)
            UserAnswer(test=test, question=question, answer=q['user_answer'])

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

#TODO move this
@test_bp.route('/tmp/<int:test_id>', methods=['GET', 'POST'])
@login_required
@db_session
def old_test(test_id):
    if request.method == 'POST':
        test = Test.get(id=test_id)
        if not test:
            abort(404)
        if current_user != test.for_user:
            abort(403)
        answers = []
        for q in test.questions:
            answers.append(UserAnswer(test=test, question=q, answer=request.form.get(str(q.id))))
        test.user_answers = answers
        test.completed = True
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
