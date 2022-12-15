from flask import render_template, redirect, flash, url_for, request, abort, send_file
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import and_, or_, not_

from app import app, db
from app.bps.settings import bp
from app.bps.settings.forms import SettingsForm
from app.models import User, UserTag, Recipt, Tag, Share


@bp.route('/', methods=["GET", "POST"])
@login_required
def index():
    form = SettingsForm()

    if form.validate_on_submit():
        print(form.logging.data)

    return render_template("settings.html", title="Indstillinger", form=form)
