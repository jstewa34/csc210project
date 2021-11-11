from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, ValidationError
from wtforms.validators import DataRequired, Email

from models import User


class login_form(FlaskForm):
    email = StringField('Username:', validators=[DataRequired()])
    password_hash = PasswordField('Password:', validators=[DataRequired()])


class register_form(FlaskForm):
    fname = StringField('First Name:', validators=[DataRequired()])
    lname = StringField('Last Name:', validators=[DataRequired()])
    email = StringField('Email address: ', validators=[
                        DataRequired(), Email()])
    password_hash = PasswordField(validators=[DataRequired()])

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Uh oh! This email is already in use.")
