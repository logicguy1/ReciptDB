from flask import Blueprint

bp = Blueprint('api', __name__)

from app.bps.api import routes
