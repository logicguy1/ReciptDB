from flask_wtf import FlaskForm
from wtforms import widgets, StringField, PasswordField, BooleanField, SubmitField, FileField, SelectField, TextAreaField, SelectMultipleField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, regexp
from app.models import User

import re


class CreateInviteForm(FlaskForm):
    code = StringField("Invitations Kode", validators=[DataRequired()])
    submit = SubmitField("Tilføj")


class SetInviteForm(FlaskForm):
    code = StringField("")
    activate = BooleanField("")
    submit = SubmitField("")


class ChangePasswordForm(FlaskForm):
    password = PasswordField("New password", validators=[DataRequired()])
    acc = HiddenField("account")
    submit = SubmitField("Opdater")


class DeleteUserForm(FlaskForm):
    code_del = StringField("")
    submit = SubmitField("")
