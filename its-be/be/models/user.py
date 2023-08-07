from pony.orm import Required, Set, PrimaryKey, Optional
from datetime import date
from flask_login import UserMixin
from .database import db

class User(db.Entity, UserMixin):
    username = PrimaryKey(str)
    password = Required(str)
    enrolled_courses = Set('Course')
    dob = Required(date)
    tests = Set('Test')
    def get_id(self):
        return self.username
