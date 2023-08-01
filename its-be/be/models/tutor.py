from pony.orm import Required, Set, Optional, PrimaryKey
from .database import db
from .user import User

class Course(db.Entity):
    name = Required(str)
    tests = Set('Test')
    questions = Set('Question')
    enrolled_users = Set(User)

class Test(db.Entity):
    course = Required(Course)
    questions = Set('Question')
    user_answers = Set('UserAnswer')
    for_user = Required(User)
    ready = Required(bool, default=False)
    completed = Required(bool, default=False)

class Question(db.Entity):
    course = Required(Course)
    tests = Set(Test)
    question = Required(str)
    answer = Required(str)
    options = Set('Option')
    difficulty = Required('Difficulty')
    tags = Set('Tag')
    explanation = Required(str)
    age_range = Required('AgeRange')
    user_answers = Set('UserAnswer')

class Option(db.Entity):
    question = Required(Question)
    option = Required(str)

class Tag(db.Entity):
    tag = PrimaryKey(str)
    question = Set(Question)

class UserAnswer(db.Entity):
    test = Required(Test)
    question = Required(Question)
    answer = Required(str)

class AgeRange(db.Entity):
    start = Required(int)
    end = Required(int)
    PrimaryKey(start, end)
    questions = Set(Question)

class Difficulty(db.Entity):
    difficulty = PrimaryKey(int)
    questions = Set(Question)
