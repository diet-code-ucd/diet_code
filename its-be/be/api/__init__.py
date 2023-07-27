from flask import Blueprint

from . import course

bp = Blueprint('api', __name__, url_prefix='/api')
bp.register_blueprint(course.bp)
# bp.register_blueprint(test.bp)




