from flask import Blueprint

bp = Blueprint('stats', __name__)

from app.bps.stats import routes
