from flask import Blueprint, render_template
from flask_login import login_required, current_user
from pony.flask import db_session

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)