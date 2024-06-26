import json

from flask import Blueprint, abort, jsonify, redirect, render_template, request, url_for
from flask import Blueprint, abort, jsonify, render_template, request
from flask_login import login_required, current_user
from pony.flask import db_session

from .models import Course, Test, Question, UserAnswer

views = Blueprint('views', __name__)
course = Blueprint('course', __name__)

@views.route('/', methods=['GET', 'POST'])
#@login_required
def home():
    #available_courses = Course.select(all)
    return render_template("home.html")#, #available_courses)

@views.route('/home_login', methods=['GET', 'POST'])
@login_required
def home_login():
    enrolled_courses = current_user.enrolled_courses
    available_courses = Course.select(lambda c: c not in enrolled_courses)
    return render_template("home_login.html", enrolled_courses=enrolled_courses, available_courses=available_courses)

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

@views.route('/course', methods=['GET', 'POST'])
def availableCourses():
    return render_template("course.html")


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
    return render_template("user_stats.html")

@views.route('/submit_test', methods=['GET', 'POST'])
@login_required
def submit_test():
    test_id=request.args.get('test_id') 
    return render_template("submit_test.html", test_id=test_id)

    
@views.route('/aboutus', methods=['GET', 'POST'])
@login_required
def about_us():
    return render_template("about_us.html")
