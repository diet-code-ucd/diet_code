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

    def get_tag_stats_for_course(self, course_id):
        tests = self.tests.filter(lambda t: t.course.id == course_id)
        answered_questions = []
        for t in tests:
            answered_questions.extend(t.user_answers)
        tags_data = {}
        for q in answered_questions:
            for t in q.question.tags:
                if t.tag in tags_data:
                    if q.correct:
                        tags_data[t.tag]['correct'] += 1
                    else:
                        tags_data[t.tag]['incorrect'] += 1
                    tags_data[t.tag]['total'] += 1
                else:
                    if q.correct:
                        tags_data[t.tag] = {'correct': 1, 'incorrect': 0, 'total': 1}
                    else:
                        tags_data[t.tag] = {'correct': 0, 'incorrect': 1, 'total': 1}
        return tags_data
