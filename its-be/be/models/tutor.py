from pony.orm import Required, Set
from .database import db
from .user import User

class Course(db.Entity):
    test = Set('Test')
    enrolled_users = Set(User)

class Test(db.Entity):
    course = Required(Course)
    questions = Set('Question')
    for_user = Set(User)

class Question(db.Entity):
    tests = Set(Test)

