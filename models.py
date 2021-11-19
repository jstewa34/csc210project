from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80))
    lname = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False, unique=True)

class Castaway(db.Model):
    __tablename__ = "castaway"
    id = db.Column(db.Integer, primary_key=True)
    totalPoints = db.Column(db.Integer)
    fname = db.Column(db.String(80))
    lname = db.Column(db.String(80))
    residence = db.Column(db.String(100))
    occupation = db.Column(db.String(100))
    age = db.Column(db.Integer)
    isFireBuring = db.Column(db.Boolean)
    imgSRC = db.Column(db.String(100))
