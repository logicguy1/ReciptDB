from flask_wtf import FlaskForm
from wtforms import widgets, StringField, PasswordField, BooleanField, SubmitField, FileField, SelectField, TextAreaField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, regexp
from app.models import User

import re


class CreateInviteForm(FlaskForm):
    code = StringField("Invitations Kode", validators=[DataRequired()])
    submit = SubmitField("Tilføj")


