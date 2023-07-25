from flask import Flask, redirect, url_for, abort, request, Blueprint
from flask_login import LoginManager, login_required, login_user, logout_user
from pony.flask import Pony
from models.database import db

app = Flask(__name__)

app.config.update(dict(
    DEBUG = False,
    SECRET_KEY = 'secret_xxx',
    PONY = {
        'provider': 'sqlite',
        'filename': 'its.sqlite',
        'create_db': True
    }
))

db.bind(**app.config['PONY'])
db.generate_mapping(create_tables=True)
Pony(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.User.get(id=user_id)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.User.get(username=username, password=password)
        if user:
            login_user(user)
            return redirect(url_for('landing'))
        else:
            abort(401)
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(''))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.User.get(username=username)
        if user:
            abort(409)
        else:
            user = db.User(username=username, password=password)
            db.commit()
            login_user(user)
            return redirect(url_for('landing'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Register>
        </form>
    '''

@app.route("/landing")
@login_required
def landing():
    return "<p>Wish something was here...</p>"

