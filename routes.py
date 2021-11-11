from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    session
)

from flask_mail import Mail, Message

from datetime import timedelta

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from app import create_app, db, login_manager
from models import User
from forms import login_form, register_form


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


@app.route("/", methods=("GET", "POST"))
def index():
    return render_template("landing.html")


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
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash("Invalid Username or password!", "danger")

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
        username = form.username.data

        newuser = User(
            username=username,
            fname=fname,
            lname=lname,
            email=email,
            password_hash=generate_password_hash(password_hash),
        )

        db.session.add(newuser)
        db.session.commit()
        msg = Message('Thanks for joining Survivor',
                      sender='jcstewart1829@gmail.com', recipients=[email])
        msg.body = "Hey " + fname + " " + lname + \
            ", \n\nWe are glad you have chosen to join our Fantasy Survivor Game.\n\nHave fun!\nSurvivor Team"
        mail.send(msg)
        # TODO: Send email here :)

        flash(f"Account Succesfully created", "success")
        return redirect(url_for("login"))

    return render_template("register.html",
                           form=form
                           )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
