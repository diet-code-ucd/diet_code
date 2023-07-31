import re
from flask import Blueprint, redirect, render_template, request, url_for, abort, flash
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
        confirm_password = request.form['confirm_password']
        user = User.get(username=username)
        if user:
            abort(409)
        if password != confirm_password:
            error = "Password and password confirmation do not match."
            flash(error, category="error")
        if not is_valid_password(password):
            error = "Password must be at least 6 characters with one special character and one uppercase character."
            flash(error, category="error")
        else:
            user = User(username=username, password=generate_password_hash(password))
            db.commit()
            login_user(user)
            return redirect(url_for('views.home'))
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
            return redirect(url_for('views.home'))
        else:
            abort(401)
    return render_template('auth/login.html')

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

def is_valid_password(password):
    # At least 6 characters, one special character, and one uppercase character.
    pattern = r"^(?=.*[A-Z])(?=.*[\W_]).{6,}$"
    return re.match(pattern, password) is not None
