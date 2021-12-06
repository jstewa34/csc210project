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
    def serialize(self):
        return {
            'id': self.id,
            'fname': self.fname,
            'lname': self.lname,
            'email': self.email,
            'teamID': self.teamID,
            'password_hash': self.password_hash
        }

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

class CastawayTeam(db.Model):
    __tablename__ = "castawayteam"
    user_id = db.Column(db.Integer, primary_key=True)
    castaway1 = db.Column(db.String(100))
    castaway2 = db.Column(db.String(100))
    castaway3 = db.Column(db.String(100))
    castaway4 = db.Column(db.String(100))
    castaway5 = db.Column(db.String(100)) 
    
class castawayPoints(db.Model):
    __tablename__ = "castawayPoints"
    id = db.Column(db.Integer, primary_key=True)
    episode = db.Column(db.String(100)) 
    castaway_id = db.Column(db.Integer)
    points = db.Column(db.Integer)

class history(db.Model):
    __tablename__ = "history"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    votedOff = db.Column(db.String(100))
    episode = db.Column(db.String(100))
    summary = db.Column(db.String(100))





