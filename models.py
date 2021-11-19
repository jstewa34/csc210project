from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80))
    lname = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    teamID =  db.Column(db.Integer)
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

class CastawayTeam(db.Model):
    __tablename__ = "castawayteam"
    id = db.Column(db.Integer, primary_key=True)
    castaway1 = db.Column(db.String(100))
    castaway2 = db.Column(db.String(100))
    castaway3 = db.Column(db.String(100))
    castaway4 = db.Column(db.String(100))
    castaway5 = db.Column(db.String(100))