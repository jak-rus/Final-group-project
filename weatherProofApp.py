from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import (
    UserMixin,
    LoginManager,
    login_required,
    current_user,
    login_user,
    logout_user,
)
import random
from flask_sqlalchemy import SQLAlchemy
import os


# ---app database and login setup---
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.secret_key = os.getenv("SECRET_KEY")
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
# ----------------------------------


# ---DATABASE SETUP---
class user(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    temperature_threshold = db.Column(db.Integer, default=60)

    def get_id(self):
        return self.id

    def __repr__(self) -> str:
        return f"User: {self.username} with temperature threshold: {self.temperature_threshold}"


with app.app_context():
    db.create_all()
# --------------------


# ---landing and login pages, as well as account functionality---
@login_manager.user_loader
def load_user(id):
    return user.query.get(int(id))


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/home")
@login_required
def home():
    this_user = user.query.filter_by(username=current_user.username).first()
    threshold = this_user.temperature_threshold

    return render_template("home.html", threshold=threshold)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")

    current_user = user.query.filter_by(username=username).first()

    if not current_user:
        flash("Please check username and try again!")
        return redirect(url_for("login"))

    login_user(current_user)
    return redirect(url_for("home"))  ##CHANGE THIS TO THE HOME PAGE AFTER LOGIN


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    username = request.form.get("username")

    current_user = user.query.filter_by(username=username).first()

    if current_user:
        flash("Username already taken! Try again.")
        return redirect(url_for("signup"))

    new_account = user(username=username)
    db.session.add(new_account)
    db.session.commit()
    flash("Username successfully registered!")
    return redirect(url_for("login"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# ---------------------------------------------------------


# ---Weather API Functionality---
@app.route("/preferences")
@login_required
def preferences():
    this_user = user.query.filter_by(username=current_user.username).first()
    if this_user:
        threshold = this_user.temperature_threshold
        return render_template("preferences.html", threshold=threshold)
    else:
        return render_template("login.html")


@app.route("/preferences", methods=["POST"])
@login_required
def change_preferences_post():
    this_user = this_user = user.query.filter_by(username=current_user.username).first()
    threshold = request.form.get("threshold-setting")
    this_user.temperature_threshold = threshold
    db.session.commit()
    return redirect(url_for("preferences"))


app.run()
