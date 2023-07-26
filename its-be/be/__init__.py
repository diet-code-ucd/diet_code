from flask import Flask
from pony.flask import Pony
from flask_login import LoginManager, login_required
from .models.database import db

def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY = 'dev',
        DATABASE = {
            'provider': 'mysql',
            'host': 'localhost',
            'user': 'its_admin',
            'password': 'test123',
            'db': 'its-mysql'
        }
    )
    app.config.from_prefixed_env()

    db.bind(**app.config['DATABASE'])
    db.generate_mapping(create_tables=True)
    Pony(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return db.User.get(id=user_id)

    @app.route('/ping')
    def ping():
        return 'pong'

    @app.route('/ping/auth')
    @login_required
    def ping_auth():
        return 'authenticated pong'

    from . import auth, api
    app.register_blueprint(auth.bp)
    app.register_blueprint(api.bp)

    return app 
