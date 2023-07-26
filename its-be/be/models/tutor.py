from pony.orm import Required, Set, Optional
from .database import db
from .user import User

class Course(db.Entity):
    name = Required(str)
    test = Set('Test')
    enrolled_users = Set(User)

class Test(db.Entity):
    course = Required(Course)
    questions = Set('Question')
    user_answers = Set('UserAnswer')
    for_user = Set(User)

class Question(db.Entity):
    tests = Set(Test)
    question = Required(str)
    answer = Required(str)
    options = Set('Option')
    tags = Set('Tag')
    user_answers = Set('UserAnswer')

class Option(db.Entity):
    question = Required(Question)
    option = Required(str)

class Tag(db.Entity):
    question = Set(Question)
    tag = Required(str)

class UserAnswer(db.Entity):
    test = Required(Test)
    question = Required(Question)
    answer = Required(str)

