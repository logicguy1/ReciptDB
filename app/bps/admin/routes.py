from flask import render_template, redirect, flash, url_for, request, abort, send_file
from flask_login import current_user, login_user, logout_user, login_required
from flask_uploads import configure_uploads, IMAGES, UploadSet
from werkzeug.urls import url_parse

from sqlalchemy import and_, or_, not_
from datetime import datetime
import os
import uuid

from app import app, db
from app.bps.admin import bp
from app.bps.admin.forms import CreateInviteForm, SetInviteForm
from app.models import User, UserTag, Recipt, Tag, Invite


@bp.route('/', methods=["GET", "POST"])
@login_required
def index():
    if not current_user.is_admin(): abort(404)

    form = CreateInviteForm()
    if form.validate_on_submit():
        code = form.code.data
        i = Invite(code=code, status=0, user_id=None)
        db.session.add(i)
        db.session.commit()
        flash("infoTilføjet ny invitations kode")
        return redirect(url_for("admin.index"))

    invites = Invite.query.order_by(Invite.status.desc()).all()

    form.code.data = uuid.uuid4()
    form2 = SetInviteForm()
    return render_template("admin/index.html", form=form, form2=form2, codes=invites)


@bp.route('/enable', methods=["POST"])
@login_required
def toggle():
    form = SetInviteForm()

    if form.validate_on_submit():
        code = Invite.query.filter_by(code=form.code.data).first_or_404()
        state = form.activate.data

        if state:
            code.status = 2
        else:
            if code.author:
                code.status = 1
            else:
                code.status = 0

        db.session.commit()

    return redirect(url_for("admin.index"))
