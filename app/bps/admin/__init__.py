from flask import Blueprint

bp = Blueprint('admin', __name__)

from app.bps.admin import routes
