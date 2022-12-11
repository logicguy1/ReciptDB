from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, SelectField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, regexp
from app.models import User

import re


def get_recipe_form(tags: list) -> FlaskForm:
    class AddReciptForm(FlaskForm):
        store = StringField("Store", validators=[DataRequired()])
        total = StringField("Total", validators=[DataRequired()])
        image = FileField(u'Image File', validators=[])
        submit = SubmitField("Upload")

        # def validate_image(form, field):
        #     if field.data:
        #         field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)

    tags = tags + ["No tag"]
    setattr(AddReciptForm, "tags", SelectField("Tags", choices=tags))

    return AddReciptForm()


def get_edit_form(recipt):
    class EditRecipeForm(FlaskForm):
        submit = SubmitField("Gem ændringer")

    setattr(EditRecipeForm, "timestamp", StringField("Timestamp", validators=[DataRequired()], default=recipt.timestamp))
    setattr(EditRecipeForm, "body", TextAreaField("Body", validators=[DataRequired()], default=recipt.body))
    setattr(EditRecipeForm, "total", StringField("Total", validators=[DataRequired()], default=recipt.total))

    return EditRecipeForm()

