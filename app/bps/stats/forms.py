from flask_wtf import FlaskForm
from wtforms import widgets, StringField, PasswordField, BooleanField, SubmitField, FileField, SelectField, TextAreaField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, regexp
from app.models import User

import re


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


def get_search_form(tags: list) -> FlaskForm:
    class SearchForm(FlaskForm):
        submit = SubmitField("Opdater")

    setattr(SearchForm, "tags", MultiCheckboxField("Tags", choices=tags, validate_choice=False))

    return SearchForm()


