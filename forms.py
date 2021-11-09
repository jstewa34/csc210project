from wtforms import (
    StringField,
    PasswordField
)

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email
from flask_login import current_user


class login_form(FlaskForm):
    email = StringField('Username:', validators=[DataRequired()])
    password_hash = PasswordField('Password:', validators=[DataRequired()])

class register_form(FlaskForm):
    fname = StringField('First Name:', validators=[DataRequired()])
    lname = StringField('Last Name:', validators=[DataRequired()])
    email = StringField('Email address: ', validators=[DataRequired(), Email()])
    username = StringField('Username:', validators=[DataRequired()])
    password_hash = PasswordField(validators=[DataRequired()])