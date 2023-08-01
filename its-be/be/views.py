from flask import Blueprint, abort, render_template, request
from flask_login import login_required, current_user
from pony.flask import db_session

from .models import Course, Test, Question, UserAnswer

views = Blueprint('views', __name__)
course = Blueprint('course', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

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
    test = Test.get(id=1)
    return render_template("user_test.html", user=current_user, course_id=course_id, test=test)

@views.route('/userstats', methods=['GET', 'POST'])
@login_required
def userStats():
    return render_template("user_stats.html")
