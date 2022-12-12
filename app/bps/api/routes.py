from flask import render_template, redirect, flash, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import db
from app.bps.api import bp
from app.models import User, UserTag, Recipt, Tag

@bp.route('/upload', methods=["GET", "POST"])
def index():
    return jsonify({"Hi": "Woah"})
