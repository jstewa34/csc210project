from datetime import timedelta

from flask import Flask, flash, redirect, render_template, session, url_for
from flask_login import (LoginManager, UserMixin, current_user, login_required, login_user, logout_user)
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash

from app import create_app, db, login_manager
from forms import login_form, register_form, make_team
from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app = create_app()
app.config['SECRET_KEY'] = "1234"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'survivorCSC214@gmail.com'
app.config['MAIL_PASSWORD'] = 'UofRSurvivor214'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

@app.route("/startgame", methods=("GET", "POST"))
def game():
    return render_template("game-page.html")

@app.route("/login/", methods=("GET", "POST"))
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.password_hash, form.password_hash.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Invalid email or password!", "danger")
        except Exception as e:
            flash("Invalid email or password!", "danger")

    return render_template("login.html", form=form)

# Register route


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
        # Email
        # msg = Message('Thanks for joining Survivor', sender='jcstewart1829@gmail.com', recipients=[email])
        # msg.body = "Hey " + fname + " " + lname + \
        #     ", \n\nWe are glad you have chosen to join our Fantasy Survivor Game.\n\nHave fun!\nSurvivor Team"
        # mail.send(msg)

        flash(f"Account Succesfully created", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)

@app.route("/", methods=("GET", "POST"))
def index():
    form = make_team()
    castaways = ["Name1", "Name2", "Name3", "Name4", "Name5"]
    if form.validate_on_submit():
        castaways[0] = form.castaway1.data
        castaways[1] = form.castaway2.data
        castaways[2] = form.castaway3.data
        castaways[3] = form.castaway4.data
        castaways[4] = form.castaway5.data
        good = True
        for i in castaways:
            # Check if all names r in the BD
        for i in range(len(castaways)):
            for j in range(i + 1, len(castaways)):
                if(castaways[i] == castaways[j]):
                   good = False 

        if good:          
            return render_template("game-page.html")
        else:
            # Send Alert here
            return render_template("landing.html", form=form, castaways=castaways)
    return render_template("landing.html", form=form, castaways=castaways)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
