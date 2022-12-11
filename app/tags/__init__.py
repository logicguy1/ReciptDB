from flask import Blueprint

bp = Blueprint('tags', __name__)

from app.tags import routes
