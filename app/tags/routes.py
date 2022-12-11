from flask import render_template, redirect, flash, url_for, request, abort, send_file
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from datetime import datetime
import os

from app import app, db
from app.tags import bp
# from app.tags.forms import get_recipe_form, get_edit_form
from app.models import User, UserTag, Recipt, Tag
# from app.cv2_model import process_image

@bp.route('/tags', methods=["GET", "POST"])
@login_required
def index():
    r = current_user.recipts.all()
    return "Okay fair"
    return render_template("dashboard/main.html", recipts=r)
