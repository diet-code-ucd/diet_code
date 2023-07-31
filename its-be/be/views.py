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
    if not course:
        abort(404)  
    return render_template("course_details.html", course = course.to_dict())
