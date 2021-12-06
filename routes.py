from datetime import timedelta

from flask import Flask, flash, redirect, render_template, session, url_for, jsonify
from flask_login import (LoginManager, UserMixin, current_user, login_required, login_user, logout_user)
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash

from flask_bootstrap import Bootstrap
from flask_moment import Moment

from app import create_app, db, login_manager
from forms import login_form, register_form, make_team
from models import User, Castaway, CastawayTeam, history, castawayPoints
import json
from api import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app = create_app()
# Email Stuff (uncomment later)
# app.config['SECRET_KEY'] = "1234"
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'survivorCSC214@gmail.com'
# app.config['MAIL_PASSWORD'] = 'UofRSurvivor210'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)

bootstrap = Bootstrap(app)
moment = Moment(app)

@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

@app.route("/startgame", methods=("GET", "POST"))
def game():
    jLen = getPoints()
    hist = db.session.query(history).all()
    points =  db.session.query(castawayPoints).all()
    x = len(db.session.query(CastawayTeam).all()) == len(db.session.query(User).all())
    if current_user.is_authenticated & x:
        team = db.session.query(CastawayTeam).get(current_user.id)
        t = []
        ids = []
        for c in db.session.query(Castaway).all():
            if(team.castaway1 == c.fname):
                ids.append(c.id)
                t.append(c)
            if (team.castaway2 == c.fname):
                ids.append(c.id)
                t.append(c)
            if (team.castaway3 == c.fname): 
                ids.append(c.id)
                t.append(c)
            if (team.castaway4 == c.fname): 
                ids.append(c.id)
                t.append(c)
            if (team.castaway5 == c.fname):
                ids.append(c.id)
                t.append(c)
        totalPoints = 0
        z = 0
        x = 0
        castPoints = [0, 0, 0, 0, 0]
        for i in ids:
            for p in points:
                if (i == p.castaway_id):
                    if (z == jLen):
                        z = 1
                        x = x + 1
                    else:
                        z = z + 1
                    print(x)
                    print(castPoints)
                    print(ids)
                    print(points)
                    print()
                    castPoints[x] = castPoints[x] + p.points
                    totalPoints = totalPoints + p.points
        return render_template("game-page.html", team=t, histroy=hist, totPoints = totalPoints, castPoints=castPoints)
    return redirect(url_for("index"))

@app.route("/chooseteam", methods=("GET", "POST"))
def chooseteam():
    form = make_team()
    x = len(db.session.query(CastawayTeam).all()) != len(db.session.query(User).all())
    if current_user.is_authenticated & x:
        chosen = []
        if form.validate_on_submit():
            chosen.append(form.castaway1.data)
            chosen.append(form.castaway2.data)
            chosen.append(form.castaway3.data)
            chosen.append(form.castaway4.data)
            chosen.append(form.castaway5.data)
            good = True
            # Check for no repeated names
            for i in range(len(chosen)):
                for j in range(i + 1, len(chosen)):
                    if(chosen[i] == chosen[j]):
                       good = False 
            if good: 
                newcastawayteam = CastawayTeam(
                    user_id = current_user.id,
                    castaway1 = form.castaway1.data,
                    castaway2 = form.castaway2.data,
                    castaway3 = form.castaway3.data,
                    castaway4 = form.castaway4.data,
                    castaway5 = form.castaway5.data
                )
                db.session.add(newcastawayteam)
                db.session.commit()
                return redirect(url_for("game"))
            else:
                # Send Alert here that there is a repeat player
                return render_template("choose-team.html", form=form, castaways=db.session.query(Castaway).all())

    else:
        return redirect(url_for("index"))
    return render_template("choose-team.html", form=form, castaways=db.session.query(Castaway).all())

@app.route("/login/", methods=("GET", "POST"))
def login():
    form = login_form()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.password_hash, form.password_hash.data):
                login_user(user)
                if(db.session.query(CastawayTeam).get(user.id) == None):
                    return redirect(url_for('chooseteam'))
                else:
                    return redirect(url_for("game"))
            else:
                flash("Invalid email or password!", "danger")
        except Exception as e:
            flash("Invalid email or password!", "danger")
    return render_template("login.html", form=form)

@app.route("/register/", methods=("GET", "POST"))
def register():
    form = register_form()
    if form.validate_on_submit():
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        password_hash = form.password_hash.data
        newuser = User(
            fname=fname,
            lname=lname,
            email=email,
            password_hash=generate_password_hash(password_hash),
        )
        db.session.add(newuser)
        db.session.commit()

        # Email Stuff (create new account before truning in)
        # msg = Message('Thanks for joining Survivor', sender='jcstewart1829@gmail.com', recipients=[email])
        # msg.body = "Hey " + fname + " " + lname + ", \n\nWe are glad you have chosen to join our Fantasy Survivor Game.\n\nHave fun!\nSurvivor Team"
        # mail.send(msg)

        flash("Account Succesfully created", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)

@app.route("/", methods=("GET", "POST"))
def index():
    return render_template("landing.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

def getPoints():
    pointsJSON = json.load(open('static/points.json'))
    if (0 == len(db.session.query(castawayPoints).all())):
        for i in pointsJSON:
            c = pointsJSON[i]
            count = 0
            for x in c["points"]:
                count = count + 1
                newCastPoints = castawayPoints(
                    episode = i, 
                    castaway_id = count,
                    points = x
                )        
                db.session.add(newCastPoints)
            db.session.commit()
    else:
        if(18 * len(pointsJSON) != len(db.session.query(castawayPoints).all())):
            count = len(pointsJSON)
            for i in pointsJSON:
                count = count - 1
                c = pointsJSON[i]
                if(count == 0):
                    for x in c["points"]:
                        count = count + 1
                        newCastPoints = castawayPoints(
                            episode = i, 
                            castaway_id = count,
                            points = x
                        )        
                        db.session.add(newCastPoints)
                    db.session.commit()
    return len(pointsJSON)


@app.route('/api/getUserById/<id>', methods=['GET'])
def get_user_by_id(id):
   return getUserById(id)

@app.route('/api/getAllUsers', methods=['GET'])
def get_all_users():
   return getAllUsers()

if __name__ == "__main__":
    app.run(debug=True)
