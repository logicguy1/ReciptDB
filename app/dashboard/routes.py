from flask import render_template, redirect, flash, url_for, request, abort, send_file
from flask_login import current_user, login_user, logout_user, login_required
from flask_uploads import configure_uploads, IMAGES, UploadSet
from werkzeug.urls import url_parse

from datetime import datetime
import os

from app import app, db
from app.dashboard import bp
from app.dashboard.forms import get_recipe_form, get_edit_form
from app.models import User, UserTag, Recipt, Tag
from app.cv2_model import process_image


images = UploadSet('images', IMAGES)
configure_uploads(app, images)


@bp.route('/', methods=["GET", "POST"])
@bp.route('/index', methods=["GET", "POST"])
@login_required
def index():
    r = current_user.recipts.all()
    return render_template("dashboard/main.html", recipts=r)


@bp.route('/create', methods=["GET", "POST"])
@login_required
def add():
    r = current_user.recipts.all()
    tags = [(i.id, i.body) for i in current_user.tags.all()]
    form = get_recipe_form(tags)

    if form.validate_on_submit():
        filename = images.save(form.image.data)
        text, file_name = process_image(filename)

        r = Recipt(
                user_id=current_user.id,
                store=form.store.data,
                body=text[:4000],
                timestamp=datetime.now().strftime(app.config["TIME_STR"]),
                img_src=file_name,
                total=form.total.data,
            ) 
        db.session.add(r)

        u_tag_id = current_user.tags.filter_by(body=form.tags.data).first()
        if u_tag_id is not None:
            t = Tag(recipt_id=r.id, user_tag_id=u_tag_id)
            db.session.add(t)

        db.session.commit()

        return redirect(url_for("dashboard.index"))

    return render_template("dashboard/new.html", form=form)


@bp.route('/view', methods=["GET", "POST"])
@login_required
def view():
    args = request.args
    recipt_id = args.get("id")
    
    if recipt_id is None:
        return abort(404)

    r = Recipt.query.filter_by(id=recipt_id, user_id=current_user.id).first_or_404()

    form = get_edit_form(r)

    if form.validate_on_submit():
        r.timestamp = form.timestamp.data
        r.body = form.body.data
        r.total = form.total.data
        db.session.commit()

        return redirect(url_for("dashboard.index"))


    return render_template("dashboard/view.html", recipt=r, form=form)


@bp.route('/img')
@login_required
def img():
    args = request.args
    recipt_id = args.get("id")
    cool = args.get("cool")
    
    if recipt_id is None:
        return abort(404)

    file_name = Recipt.query.filter_by(id=recipt_id, user_id=current_user.id).first_or_404().img_src

    return send_file("assets/recipts/" + ("masked_" if cool == "1" else "") + file_name, mimetype='image/gif')


@bp.route('/delete')
@login_required
def delete():
    args = request.args
    recipt_id = args.get("id")

    if recipt_id is None:
        return abort(404)

    r = Recipt.query.filter_by(id=recipt_id, user_id=current_user.id)
    data = r.first_or_404()
    tags = data.tags.delete()
    
    os.remove(f'app/assets/recipts/{data.img_src}') 

    r.delete()
    db.session.commit()

    return redirect(url_for("dashboard.index"))
