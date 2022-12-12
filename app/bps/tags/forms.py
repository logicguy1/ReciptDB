from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, SelectField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, regexp, Length
from app.models import User

import re


class NewTagForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    color = StringField("Color", validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField("Gem")

    def validate_color(self, color):
        color = color.data
        if len(color) != 6:
            raise ValidationError('Must be a valid color code (6 charecters)')

        for i in color:
            if i.upper() not in "0123456789ABCDEF":
                raise ValidationError('Must be a valid color code (Only hexadecimal charecters allowed).')



class SearchForm(FlaskForm):
    search = StringField("Search", default="")
    submit = SubmitField("Søg")


