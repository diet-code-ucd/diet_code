from celery import shared_task
from flask import Blueprint, jsonify, redirect, render_template, request, url_for, abort
from flask_login import login_required, current_user
from pony.flask import db_session
import random
from datetime import date

from pony.orm import commit, flush

from .models import Course, Test, Question, UserAnswer, Topic, Option
from .ml import generate_questions



from celery import shared_task
from pony.flask import db_session


@shared_task()
@db_session
def add_questions_to_test(test_id):
    test = Test.get(id=test_id)
    user_course_selection = test.user_course_selection
    user = user_course_selection.user
    course = user_course_selection.course
    user_age = date.today().year - user.dob.year
    questions = Question.select().where(course=course)
    available_questions = []
    for q in questions:
        if user not in q.tests.user_course_selection.user:
            age_range = q.age_range.split('-')
            if int(age_range[0]) <= user_age <= int(age_range[1]):
                available_questions.append(q)
    if len(available_questions) < 7:
        generate_result = generate_questions(course.name, user_age, test.topics.topic)
        for q in generate_result.questions:
            topics = []
            for t in q.topics:
                topic = Topic.get(topic=t)
                if topic:
                    topics.append(topic)
                else:
                    topics.append(Topic(topic=t))
            question = Question(course=course, question=q.question, answer=q.answer, age_range=q.ageRange, difficulty=q.difficulty, explanation=q.explanation, topics=topics)
            
            options = [Option(option=o, question=question) for o in q.options]
            available_questions.append(question)
        commit()
    available_questions = random.sample(available_questions, 7)
    test.questions = available_questions
    test.ready = True

