from flask import Flask
from pony.flask import Pony
from flask_login import LoginManager, login_required
from .models import db, User
from celery import Celery, Task

def init_app(worker=False) -> Flask:
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY = 'dev',
        DATABASE = {
            'provider': 'mysql',
            'host': 'localhost',
            'user': 'its_admin',
            'password': 'test123',
            'db': 'its-mysql'
        },
        QUEUE = {
            'broker_url': 'redis://localhost:6379/0',
            'result_backend': 'redis://localhost:6379/0',
            'task_ignore_result': True,
            'task_serializer': 'pickle',
            'accept_content': ['pickle'],
        },
    )
    app.config.from_prefixed_env()
    celery_init_app(app)

    with app.app_context():
        db.bind(**app.config['DATABASE'])
        db.generate_mapping(create_tables=True)
        Pony(app)

        login_manager = LoginManager(app)
        login_manager.login_view = 'auth.login'

        @login_manager.user_loader
        def load_user(user_username):
            return User.get(username=user_username)

        @app.route('/ping')
        def ping():
            return 'pong'

        @app.route('/ping/auth')
        @login_required
        def ping_auth():
            return 'authenticated pong'

        from . import auth, api, views

        app.register_blueprint(auth.bp)
        app.register_blueprint(api.bp)
        app.register_blueprint(views.views)
        app.register_blueprint(views.course)

        return app 

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["QUEUE"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
