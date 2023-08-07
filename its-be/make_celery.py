from be import init_app

flask_app = init_app(True)
celery_app = flask_app.extensions['celery']

