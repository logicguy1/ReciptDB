from flask import render_template, redirect, flash, url_for, request, abort, send_file
from flask_login import current_user, login_user, logout_user, login_required
from flask_uploads import configure_uploads, IMAGES, UploadSet
from werkzeug.urls import url_parse

from sqlalchemy import and_, or_, not_
from datetime import datetime
import os

from app import app, db
from app.bps.dashboard import bp
from app.bps.dashboard.forms import get_recipe_form, get_edit_form, SearchForm
from app.models import User, UserTag, Recipt, Tag, Share
from app.cv_models.cv2_model import process_image


images = UploadSet('images', IMAGES)
configure_uploads(app, images)


@bp.route('/', methods=["GET", "POST"])
@bp.route('/index', methods=["GET", "POST"])
@login_required
def index():
    form = SearchForm()

    if form.validate_on_submit():
        r = current_user.recipts.filter(
                or_(
                    Recipt.body.like(f"%{form.search.data}%"),
                    Recipt.timestamp.like(f"%{form.search.data}%"),
                    Recipt.store.like(f"%{form.search.data}%"),
                    Recipt.total.like(f"%{form.search.data}%")
                )).order_by(Recipt.timestamp.desc()
            ).all()
    else:
        r = current_user.recipts.order_by(Recipt.timestamp.desc()).all()

    return render_template("dashboard/main.html", title="Bonner", recipts=r, form=form)


@bp.route('/create', methods=["GET", "POST"])
@login_required
def add():
    r = current_user.recipts.all()
    tags = [(i.id, i.body) for i in current_user.tags.all()]
    form = get_recipe_form(tags)

    if form.validate_on_submit():
        if form.image.data:
            filename = images.save(form.image.data)
            text, file_name = process_image(filename)
        else:
            text = "Ingen bon"
            file_name = None

        r = Recipt(
                user_id=current_user.id,
                store=form.store.data,
                body=text[:4000],
                #timestamp=datetime.now().strftime(app.config["TIME_STR"]),
                img_src=file_name,
                total=form.total.data,
            ) 
        db.session.add(r)

        print(form.tags.data)
        u_tag_id = current_user.tags.filter_by(id=form.tags.data).first()
        if u_tag_id is not None:
            t = Tag(recipt_id=r.id, user_tag_id=u_tag_id.id)
            db.session.add(t)

        db.session.commit()

        return redirect(url_for("dashboard.index"))

    return render_template("dashboard/new.html", title="Upload", form=form)


@bp.route('/view', methods=["GET", "POST"])
@login_required
def view():
    args = request.args
    recipt_id = args.get("id")
    new_tag = args.get("add_tag")
    rem_tag = args.get("rem_tag")
    
    if recipt_id is None:
        return abort(404)

    r = Recipt.query.filter_by(id=recipt_id, user_id=current_user.id).first_or_404()

    # If the user prompts to add a tag
    if new_tag is not None:
        t = current_user.tags.filter_by(id=new_tag).first_or_404()
        tag = Tag(recipt_id=r.id, user_tag_id=t.id)
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for("dashboard.view", id=r.id))

    # If the user prompts to remove a tag
    if rem_tag is not None:
        t = r.tags.filter_by(id=rem_tag).delete()
        db.session.commit()
        return redirect(url_for("dashboard.view", id=r.id))

    tags = [UserTag.query.filter_by(id=i.user_tag_id).first() for i in r.tags.all()]

    form = get_edit_form(r)

    if form.validate_on_submit():
        r.timestamp = datetime.strptime(form.timestamp.data, app.config["TIME_STR"])
        r.body = form.body.data
        r.total = form.total.data
        db.session.commit()

        return redirect(url_for("dashboard.index"))

    link = url_for("dashboard.share", share_id=r.get_share_link())
    print(link)
    all_tags = [i for i in current_user.tags.all() if i not in tags]
    return render_template(
            "dashboard/view.html", 
            title="Viser bon", 
            recipt=r, 
            form=form, 
            tags=list(zip(tags, r.tags.all())), 
            all_tags=all_tags,
            link=link,
        )


@bp.route('/img')
def img():
    args = request.args
    recipt_id = args.get("id")
    code = args.get("share")
    
    if recipt_id is None:
        return abort(404)

    # If the user is logged in just make the normal query
    if current_user.is_authenticated:
        file_name = Recipt.query.filter_by(id=recipt_id, user_id=current_user.id).first_or_404().img_src
        return send_file("assets/recipts/" + file_name, mimetype='image/gif')
    else:
        r = Recipt.query.filter_by(id=recipt_id).first_or_404()
        s = r.share.first_or_404().code
        if code == s:
            file_name = r.img_src
            return send_file("assets/recipts/" + file_name, mimetype='image/gif')
    
    abort(404)



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


@bp.route('/share/<share_id>')
def share(share_id):
    share = Share.query.filter_by(code=share_id).first_or_404()
    return render_template(
            "dashboard/share.html",
            title="Bon",
            share=share,
            )
