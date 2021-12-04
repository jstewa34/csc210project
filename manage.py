from app import db
import json
from models import Castaway, history

# python3 manage.py
def deploy():
    from app import create_app, db
    from models import User
    app = create_app()
    app.app_context().push()
    db.create_all()

deploy()

# Creates Castaway DB Table
castawaysJSON = json.load(open('static/castaways.json'))
count = 0
for r in db.session.query(Castaway).all():
    count = count + 1
if (count == 0):
    for i in castawaysJSON:
        c = castawaysJSON[i]
        newcastaway = Castaway(
            fname = i,
            lname = c["lname"],
            residence = c["residence"],
            occupation = c["occupation"],
            age = c["age"],
            imgSRC = c["imgsrc"],
            isFireBuring = True,
            totalPoints = 0
        )
        db.session.add(newcastaway)
    db.session.commit()
    
historyJSON = json.load(open('static/history.json'))
count = 0
for r in db.session.query(history).all():
    count = count + 1
if (count == 0):
    for i in historyJSON:
        c = historyJSON[i]
        newHistory = history(
            date = c["date"],
            votedOff = c["votedOff"],
            episode = i,
            summary = c["summary"]
        )
        db.session.add(newHistory)
    db.session.commit()
    
