from flask import Blueprint

bp = Blueprint('settings', __name__)

from app.bps.settings import routes
