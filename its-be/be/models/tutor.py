from pony.orm import LongStr, Required, Set, Optional, PrimaryKey
from .database import db
from .user import User

class Course(db.Entity):
    name = Required(str)
    tests = Set('Test')
    questions = Set('Question')
    enrolled_users = Set(User)
    topics = Set('Topic')

class Test(db.Entity):
    course = Required(Course)
    questions = Set('Question')
    user_answers = Set('UserAnswer')
    for_user = Required(User)
    ready = Required(bool, default=False)
    completed = Required(bool, default=False)
    topics = Set('Topic')

class Question(db.Entity):
    course = Required(Course)
    tests = Set(Test)
    question = Required(LongStr, lazy=False)
    answer = Required(str)
    options = Set('Option')
    difficulty = Required(int)
    topics = Set('Topic')
    explanation = Required(LongStr, lazy=False)
    age_range = Required(str)
    user_answers = Set('UserAnswer')

class Option(db.Entity):
    question = Required(Question)
    option = Required(str)

class Topic(db.Entity):
    topic = PrimaryKey(str)
    question = Set(Question)
    test = Set(Test)

class UserAnswer(db.Entity):
    test = Required(Test)
    question = Required(Question)
    answer = Required(str)
    correct = Required(bool)
