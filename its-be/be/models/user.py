from pony.orm import Required, Set
from flask_login import UserMixin
from .database import db


class User(db.Entity, UserMixin):
    username = Required(str, unique=True)
    password = Required(str)
    enrolled_courses = Set("Course")
    tests = Set("Test")
