from flask import Blueprint, redirect, render_template, request, url_for, abort
from flask_login import LoginManager, login_required, login_user, logout_user
from pony.flask import db_session
from werkzeug.security import check_password_hash, generate_password_hash

from .models import db, User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route("/register", methods=['GET', 'POST'])
@db_session
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get(username=username)
        if user:
            abort(409)
        else:
            user = User(username=username, password=generate_password_hash(password))
            db.commit()
            login_user(user)
            return redirect(url_for('ping_auth'))
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get(username=username)
        if user:
            if not check_password_hash(user.password, password):
                abort(401)
            login_user(user)
            return redirect(url_for('ping_auth'))
        else:
            abort(401)
    return render_template('auth/login.html')

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
