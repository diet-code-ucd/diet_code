from flask import Blueprint

from . import tests_api

bp = Blueprint("api", __name__, url_prefix="/api")
# bp.register_blueprint(course.bp)
bp.register_blueprint(tests_api.bp)
