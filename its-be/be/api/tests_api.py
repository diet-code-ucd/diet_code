from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from pony.flask import db_session

bp = Blueprint("tests", __name__, url_prefix="/tests")

@bp.route("", methods=["GET"])
@login_required
@db_session
def get_tests():
    return jsonify([c.to_dict() for c in current_user.tests])
