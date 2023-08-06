import json

from flask import Blueprint, abort, jsonify, redirect, render_template, request, url_for
from flask import Blueprint, abort, jsonify, render_template, request
from flask_login import login_required, current_user
from pony.flask import db_session
from pony.orm import select
from be.ml import generate_learning_material

from be.stats import get_topics_for_learning_material

from .models import Course, Test, Question, UserAnswer, Topic

views = Blueprint('views', __name__)
course = Blueprint('course', __name__)

@views.route('/', methods=['GET'])
def default():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    return render_template('auth/login.html')

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    enrolled_courses = current_user.enrolled_courses
    available_courses = Course.select(lambda c: c not in enrolled_courses)
    return render_template("user_home.html", enrolled_courses=enrolled_courses, available_courses=available_courses)

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
    topics = [] 
    for t in Topic.select().where(lambda t: t in course.questions.topics):
        topics.append(t.topic)
    return render_template("user_test.html", user=current_user, course_id=course_id, test=test, course=course, topics=topics)

@views.route('/userstats', methods=['GET', 'POST'])
@login_required
def userStats():
    return render_template("user_stats.html")

@views.route('/learning', methods=['GET'])
@login_required
def learning():
    course_id=request.args.get('course_id')
    course = Course.get(id = course_id)
    if not course:
        abort(404)
    if course not in current_user.enrolled_courses:
        abort(403)
    topics = get_topics_for_learning_material(current_user, course)
    learning_material = generate_learning_material(course.name, topics)
    return render_template("learning.html", learning_material=learning_material, course=course)

@views.route('/submit_test', methods=['GET', 'POST'])
@login_required
def submit_test():
    test_id=request.args.get('test_id') 
    return render_template("submit_test.html", test_id=test_id)

    
@views.route('/aboutus', methods=['GET', 'POST'])
@login_required
def about_us():
    return render_template("about_us.html")
