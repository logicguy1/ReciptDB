from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, SelectField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, regexp
from app.models import User

import re


def get_recipe_form(tags: list) -> FlaskForm:
    class AddReciptForm(FlaskForm):
        store = StringField("Butiks navn", validators=[DataRequired()])
        total = StringField("Total (brug punktum ikke komma)", validators=[DataRequired()])
        image = FileField("Billed fil (valgfri)", validators=[])
        submit = SubmitField("Upload")

        def validate_total(self, total):
            try:
                float(total.data)
            except:
                raise ValidationError("Dit total skal være et komma eller heltal")

        def validate_image(self, image):
            if image.raw_data:
                if image.raw_data[0].filename.endswith(".png") or image.raw_data[0].filename.endswith(".jpg"):
                    pass
                else:
                    raise ValidationError("Der modtages kun .png og .jpg filer.")

        # def validate_image(form, field):
        #     if field.data:
        #         field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)

    print(tags)
    tags = tags + [[-1, "Ingen tag"]]
    setattr(AddReciptForm, "tags", SelectField("Tags", choices=tags))

    return AddReciptForm()


def get_edit_form(recipt):
    class EditRecipeForm(FlaskForm):
        submit = SubmitField("Gem ændringer")

        def validate_total(self, total):
            try:
                float(total.data)
            except:
                raise ValidationError("Dit total skal være et komma eller heltal")

    setattr(EditRecipeForm, "timestamp", StringField("Timestamp", validators=[DataRequired()], default=recipt.timestamp))
    setattr(EditRecipeForm, "body", TextAreaField("Body", validators=[DataRequired()], default=recipt.body))
    setattr(EditRecipeForm, "total", StringField("Total", validators=[DataRequired()], default=recipt.total))

    return EditRecipeForm()


class SearchForm(FlaskForm):
    search = StringField("Search", default="")
    submit = SubmitField("Søg")


