from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, SelectField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, regexp
from app.models import User
from app import app


class SettingsForm(FlaskForm):
    logging = BooleanField("Må vi bruge anonymiseret data til at forbedre og optimere vores systemer?", default="checked")
    submit = SubmitField("Gem")


