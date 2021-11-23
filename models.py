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
    fname = db.Column(db.String(80))
    lname = db.Column(db.String(80))
    totalPoints = db.Column(db.Integer)
    residence = db.Column(db.String(100))
    occupation = db.Column(db.String(100))
    age = db.Column(db.Integer)
    isFireBuring = db.Column(db.Boolean)
    imgSRC = db.Column(db.String(100))

class castawayBySeason(db.Model):
    __tablename__ = "castaway_by_season"
    id = db.Column(db.Integer, primary_key=True)
    castaway_id = db.Column(db.Integer)
    season_number = db.Column(db.Integer)

class castawayRoster(db.Model):
    __tablename__ = "castaway_roster"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    castaway_selections = db.Column(db.String(100))

class castawayPoints(db.Model):
    __tablename__ = "castawayPoints"
    id = db.Column(db.Integer, primary_key=True)
    episode = db.Column(db.Integer)
    castaway_id = db.Column(db.Integer)
    points = db.Column(db.Integer)