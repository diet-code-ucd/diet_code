from pony.orm import LongStr, Required, Set, Optional, PrimaryKey
from .database import db
from .user import User
from datetime import datetime

class Course(db.Entity):
    name = Required(str)
    enrolled_users = Set('UserCourseSelection')
    questions = Set('Question')
    topics = Set('Topic')

class UserCourseSelection(db.Entity):
    """This entity is used to track which courses a user has enrolled in.
    It tracks the user, the course, and the topics that the user has selected.
    Any test generated for this course will be based on the topics selected by the user.
    """
    user = Required(User)
    course = Required(Course)
    topics = Set('Topic')
    tests = Set('Test')
    active = Required(bool, default=True)
    PrimaryKey(user, course)

class Test(db.Entity):
    user_course_selection = Required(UserCourseSelection)
    questions = Set('Question')
    user_answers = Set('UserAnswer')
    ready = Required(bool, default=False)
    completed = Required(bool, default=False)
    topics = Set('Topic')
    date_completed = Optional(datetime)

class Question(db.Entity):
    course = Required(Course)
    tests = Set(Test)
    question = Required(LongStr, lazy=False)
    answer = Required(str)
    options = Set('Option')
    difficulty = Required(int)
    explanation = Required(LongStr, lazy=False)
    age_range = Required(str)
    user_answers = Set('UserAnswer')
    topics = Set('Topic')

class Option(db.Entity):
    question = Required(Question)
    option = Required(str)

class Topic(db.Entity):
    topic = PrimaryKey(str)
    question = Set(Question)
    course = Set(Course)
    test = Set(Test)
    user_course_selections = Set(UserCourseSelection)


class UserAnswer(db.Entity):
    test = Required(Test)
    question = Required(Question)
    answer = Required(str)
    correct = Required(bool)
