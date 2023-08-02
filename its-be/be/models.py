from datetime import date
from flask_login import UserMixin
from . import db
from typing import Set
from sqlalchemy.orm import Mapped,  mapped_column, relationship
from sqlalchemy import String

class User(db.Model, UserMixin):
    username: Mapped[str] = mapped_column(String(32), primary_key=True)
    password: Mapped[str] = mapped_column(String(64))
    enrolled_courses: Mapped[Set['Course']] = relationship(back_populates='enrolled_users')
    dob: Mapped[date] = mapped_column()
    tests: Mapped[Set['Test']] = relationship(back_populates='for_user')
    def get_id(self):
        return self.username

class Course(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(255))
    tests: Mapped[Set['Test']] = relationship(back_populates='course')
    questions: Mapped[Set['Question']] = relationship(back_populates='course')
    enrolled_users: Mapped[Set['User']] = relationship(back_populates='enrolled_courses')

class Test(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    course: Mapped[Course] = relationship(back_populates='tests')
    questions: Mapped[Set['Question']] = relationship(back_populates='tests')
    user_answers: Mapped[Set['UserAnswer']] = relationship(back_populates='test')
    for_user: Mapped[User] = relationship(back_populates='tests')
    ready: Mapped[bool] = mapped_column()
    completed: Mapped[bool] = mapped_column()

class Question(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    course: Mapped[Course] = relationship(back_populates='questions')
    tests: Mapped[Set['Test']] = relationship(back_populates='questions')
    question: Mapped[str] = mapped_column(String(255))
    answer: Mapped[str] = mapped_column(String(255))
    options: Mapped[Set['Option']] = relationship(back_populates='question')
    difficulty: Mapped[int] = mapped_column()
    tags: Mapped[Set['Tag']] = relationship(back_populates='question')
    explanation: Mapped[str] = mapped_column(String(255))
    age_range: Mapped[int] = mapped_column()
    user_answers: Mapped[Set['UserAnswer']] = relationship(back_populates='question')

class Option(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[Question] = relationship(back_populates='options')
    option: Mapped[str] = mapped_column(String(255))

class Tag(db.Model):
    tag: Mapped[str] = mapped_column(String(255), primary_key=True)
    questions: Mapped[Set['Question']] = relationship(back_populates='tags')

class UserAnswer(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    test: Mapped[Test] = relationship(back_populates='user_answers')
    question: Mapped[Question] = relationship(back_populates='user_answers')
    answer: Mapped[str] = mapped_column(String(255))
