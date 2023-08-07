from be.models.tutor import Course, Test, Question, Tag, UserAnswer
from flask import render_template
import json

from flask import Blueprint, abort, jsonify, redirect, render_template, request, url_for
from flask import Blueprint, abort, jsonify, render_template, request
from flask_login import login_required, current_user
from pony.flask import db_session
from collections import Counter
from .models import Course, Test, Question, UserAnswer, User

views = Blueprint('views', __name__)
course = Blueprint('course', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    enrolled_courses = current_user.enrolled_courses
    available_courses = Course.select(lambda c: c not in enrolled_courses)
    return render_template("home.html", enrolled_courses=enrolled_courses, available_courses=available_courses)

@course.route('/course/<int:course_id>', methods=['GET'])
@login_required
@db_session
def course_details(course_id):
    course = Course.get(id = course_id)
    user_is_enrolled = course in current_user.enrolled_courses
    print(user_is_enrolled)
    if not course:
        abort(404)  
    return render_template("course_details.html", course = course.to_dict(), enrolled=user_is_enrolled)

@views.route('/userTest', methods=['GET', 'POST'])
@login_required
def userTest():
    course_id=request.args.get('course_id')
    course = Course.get(id = course_id)
    test = Test.get(id=1)
    return render_template("user_test.html", user=current_user, course_id=course_id, test=test, course = course)

@views.route('/userstats', methods=['GET', 'POST'])
@login_required
def userStats():
    completed_tests = Test.select(
        lambda t: t.for_user == current_user and t.completed)
    completed_tests_count = len(completed_tests)
     # Get incomplete tests count
    incomplete_tests = Test.select(lambda t: t.for_user == current_user and not t.completed)
    incomplete_tests_count = incomplete_tests.count()
    completed_questions = set(
        q for test in completed_tests for q in test.questions)
    all_tags = Tag.select()
    not_completed_tags = [tag for tag in all_tags if tag not in set(
        tag for q in completed_questions for tag in q.tags)]
    lowest_not_completed_tags = Counter(
        [tag for q in Question.select(
            lambda q: q not in completed_questions) for tag in q.tags]
    ).most_common(5)
    top_completed_tags = Counter(
        [tag for q in completed_questions for tag in q.tags]).most_common(5)
    total_tests_taken = completed_tests_count + incomplete_tests_count

    return render_template(
        "user_stats.html.j2",
        completed_tests=completed_tests_count,
        total_tests_taken=total_tests_taken,
        incomplete_tests=incomplete_tests_count,
        top_completed_tags=top_completed_tags,
        lowest_not_completed_tags=lowest_not_completed_tags
    )


@views.route('/submit_test', methods=['GET', 'POST'])
@login_required
def submit_test():
    test_id=request.args.get('test_id') 
    return render_template("submit_test.html", test_id=test_id)

    
@views.route('/aboutus', methods=['GET', 'POST'])
@login_required
def about_us():
    return render_template("about_us.html")
