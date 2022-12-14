from flask import render_template, redirect, flash, url_for, request, abort, send_file
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from datetime import datetime
import os

from app import app, db
from app.bps.tags import bp
from app.bps.tags.forms import NewTagForm
from app.models import User, UserTag, Recipt, Tag
# from app.cv2_model import process_image


@bp.route('/', methods=["GET", "POST"])
@login_required
def index():
    args = request.args
    rem_id = args.get("rem")
    if rem_id is not None:
        current_user.tags.filter_by(id=rem_id).delete()
        db.session.commit()
        return redirect(url_for("tags.index"))

    tags = current_user.tags.all()
    uses = [sum([1 if tag.id in map(lambda x: x.user_tag_id, r.tags) else 0 
                for r in current_user.recipts.all()])
            for tag in tags]
    return render_template("tags/tags.html", title="Tags", tags=zip(tags, uses))


@bp.route('/create', methods=["GET", "POST"])
@login_required
def create():
    form = NewTagForm()

    if form.validate_on_submit():
        tag = UserTag(user_id=current_user.id, body=form.name.data, color=form.color.data)
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for("tags.index"))

    return render_template("tags/new.html", title="Lav nyt tag", form=form)
