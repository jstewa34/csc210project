from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, ValidationError, SubmitField, SelectField
from wtforms.validators import DataRequired, Email
from app import db
from models import User, Castaway


class login_form(FlaskForm):
    email = StringField('Username:', validators=[DataRequired()])
    password_hash = PasswordField('Password:', validators=[DataRequired()])

class make_team(FlaskForm):
    castaways = ["", "Brad", "Danny", "David", "Eric", "Deshawn", "Erika", "Genie", "Evvie", "Heather", "Jairus", "Liana", "Naseer", "Sara", "Shantel", "Sydney", "Tiffany", "Xander"]
    castaway1 = SelectField('Castaway 1:', choices=castaways)
    castaway2 = SelectField('Castaway 2:', choices=castaways)
    castaway3 = SelectField('Castaway 3:', choices=castaways)
    castaway4 = SelectField('Castaway 4:', choices=castaways)
    castaway5 = SelectField('Castaway 5:', choices=castaways)
    submit = SubmitField('Submit')


class register_form(FlaskForm):
    fname = StringField('First Name:', validators=[DataRequired()])
    lname = StringField('Last Name:', validators=[DataRequired()])
    email = StringField('Email address: ', validators=[DataRequired(), Email()])
    password_hash = PasswordField(validators=[DataRequired()])

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Uh oh! This email is already in use.")
