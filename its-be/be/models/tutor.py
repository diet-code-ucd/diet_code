from pony.orm import Required, Set, Optional
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

class Question(db.Entity):
    course = Required(Course)
    tests = Set(Test)
    question = Required(str)
    answer = Required(str)
    options = Set('Option')
    difficulty = Required(str)
    tags = Set('Tag')
    user_answers = Set('UserAnswer')

class Option(db.Entity):
    question = Required(Question)
    option = Required(str)

class Tag(db.Entity):
    question = Set(Question)
    tag = Required(str, unique=True)

class UserAnswer(db.Entity):
    test = Required(Test)
    question = Required(Question)
    answer = Required(str)

