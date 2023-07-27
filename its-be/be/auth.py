from flask import Blueprint, redirect, request, url_for, abort
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from .models import db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = db.User.get(username=username)
        if user:
            abort(409)
        else:
            user = db.User(username=username, password=generate_password_hash(password))
            db.commit()
            login_user(user)
            return redirect(url_for("ping_auth"))
    return """
        <form method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Register>
        </form>
    """


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = db.User.get(username=username)
        if user:
            if not check_password_hash(user.password, password):
                abort(401)
            login_user(user)
            return redirect(url_for("ping_auth"))
        else:
            abort(401)
    return """
        <form method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    """


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
