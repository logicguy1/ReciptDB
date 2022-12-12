from flask import render_template, redirect, flash, url_for, request, abort, send_file
from flask_login import current_user, login_user, logout_user, login_required
from flask_uploads import configure_uploads, IMAGES, UploadSet
from werkzeug.urls import url_parse
from sqlalchemy import and_, or_, not_

import datetime

from app import app, db
from app.bps.stats import bp
from app.bps.stats.forms import get_search_form
from app.models import User, UserTag, Recipt, Tag


def get_time(months, step):
    """ Get the month/year representation relative to the given date """
    tim = datetime.datetime.utcnow()
    month = int(tim.strftime("%m"))
    year = int(tim.strftime("%Y"))
    for i in range(months):
        month += step
        if month <= 0:
            year -= 1
            month = 12

    return f"{year}-{str(month).rjust(2, '0')}"


@bp.route('/', methods=["GET", "POST"])
@login_required
def index():
    all_tags = current_user.tags.filter().all()
    tags = [(tag.id, tag.body) for tag in all_tags]

    form = get_search_form(tags)

    if form.validate_on_submit():
        selected = current_user.tags.filter(
                        not_(UserTag.id.in_(form.tags.data))
                    ).all()
    else:
        selected = all_tags

    # TODO: Make this like, database queryies instead of code for more efficiancy
    # recipts = current_user.recipts.filter(
    #             not_(Recipt.tags.id.in_(
    #                     [i.id for i in all_tags]
    #                 ))
    #         ).all()

    # Get all the recipts that does not have a tag that we did not click
    recipts = []
    [[recipts.append(tag.recipt) if tag.recipt not in recipts and not
      any(map(
              lambda x: x.usr_tag not in selected, 
              tag.recipt.tags.all()
          )) else None
      for tag in usr_tag.tags.all()] for usr_tag in selected]

    total = sum([float(recipt.total) for recipt in recipts])
    
    totals = {}
    for r in recipts:
        date = r.get_month()
        if date not in totals:
            totals[date] = []

        totals[date].append(float(r.total))

    totals = dict(map(lambda x: (x[0], sum(x[1])), totals.items()))

    # Add the last 12 months as well with the total of 0, this makes sure we have at least one year of data.
    for i in range(12):
        date = get_time(i, -1) 
        if date not in totals:
            totals[date] = 0
    
    totals = sorted(totals.items(), key=lambda x: x[0])[::-1]

    print(selected)
    tags_total = {}
    tags_avg = {}
    for usr_tag in selected:
        for tag in usr_tag.tags.all():
            if tag.recipt in recipts and tag.recipt.get_month() == get_time(0, -1):
                if usr_tag not in tags_total:
                    tags_total[usr_tag] = 0

                tags_total[usr_tag] += float(tag.recipt.total)

            if tag.recipt in recipts and tag.recipt.get_month() in (
                                                                    get_time(1, -1), 
                                                                    get_time(2, -1), 
                                                                    get_time(3, -1)):
                if usr_tag not in tags_avg:
                    tags_avg[usr_tag] = []

                tags_avg[usr_tag].append(float(tag.recipt.total))
                print(tag.recipt.store, tag.recipt.total)

    # Add all the tags not found before
    for tag in selected:
        if tag not in tags_total:
            tags_total[tag] = 0
        if tag not in tags_avg:
            tags_avg[tag] = []

    # Calculate avriges
    print(tags_avg)
    tags_avg = {k: (sum(v)/len(v)) if sum(v) != 0 and len(v) != 0 else 0 for k, v in tags_avg.items()}

    print(tags_total)
    print(tags_avg)


    return render_template(
            "stats/index.html", 
            form=form, 
            total=totals, 
            tags_total=tags_total,
            tags_avg=tags_avg,
            max=max, str=str, round=round, float=float,
            higest=max(totals[:12], key=lambda x: x[1])[1],
        )
