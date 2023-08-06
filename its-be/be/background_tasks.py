from celery import shared_task
from flask import Blueprint, jsonify, redirect, render_template, request, url_for, abort
from flask_login import login_required, current_user
from pony.flask import db_session
import random
from datetime import date

from pony.orm import commit, flush

from .models import Course, Test, Question, UserAnswer, Tag, Option
from .ml import generate_questions



from celery import shared_task
from pony.flask import db_session


@shared_task()
@db_session
def add_questions_to_test(test_id):
    test = Test.get(id=test_id)
    user = test.for_user
    user_age = date.today().year - user.dob.year
    questions = Question.select().where(course=test.course)
    available_questions = []
    for q in questions:
        if test.for_user not in q.tests.for_user:
            age_range = q.age_range.split('-')
            if int(age_range[0]) <= user_age <= int(age_range[1]):
                available_questions.append(q)
    if len(available_questions) < 7:
        generate_result = generate_questions(test.course.name, user_age, test.tags.tag)
        for q in generate_result.questions:
            tags = []
            for t in q.tags:
                tag = Tag.get(tag=t)
                if tag:
                    tags.append(tag)
                else:
                    tags.append(Tag(tag=t))
            question = Question(course=test.course, question=q.question, answer=q.answer, age_range=q.ageRange, difficulty=q.difficulty, explanation=q.explanation, tags=tags)
            
            options = [Option(option=o, question=question) for o in q.options]
            available_questions.append(question)
        commit()
    available_questions = random.sample(available_questions, 7)
    test.questions = available_questions
    test.ready = True

