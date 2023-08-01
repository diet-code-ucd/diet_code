import json
from flask import Blueprint, abort, jsonify, render_template, request
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
    if request.method == 'POST':
        # Get the JSON data from the URL parameter
        data = request.args.get('data')
        data = json.loads(data)  # Convert the data to a Python dictionary

        # Process the data as needed
        questions = data.get('questions', [])
        for question in questions:
            question_id = question.get('id')
            user_answer = question.get('user_answer')
            # Do something with the question_id and user_answer

        # After processing the data, we can return a response if needed
        return jsonify({'message': 'Data processed successfully'})

    else:
        # If the method is GET, you can render the "submit_test.html" template
        return render_template('submit_test.html')
    
@views.route('/aboutus', methods=['GET', 'POST'])
@login_required
def about_us():
    return render_template("about_us.html")
