from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import *

import hashlib

def pw_hash(username, password):
    return hashlib.md5((username + "lol" + password).encode('utf-8')).hexdigest()

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    if not form.validate():
        return render_template("loginform.html", form = LoginForm())

    user = User.query.filter_by(username = form.username.data).first()
    if not user:
        return render_template("loginform.html", form = form,
                               dberrors = ["Käyttäjää ei ole olemassa"])
    if user.password != pw_hash(user.username, form.password.data):
        return render_template("loginform.html", form = form,
                               dberrors = ["Väärä salasana"])

    login_user(user)
    return redirect(url_for("index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/auth/register", methods = ["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("registerform.html", form = RegisterForm())

    form = RegisterForm(request.form)

    if not form.validate():
        return render_template("registerform.html", form = form)
    print(form)
    if db.session.query(User.id).filter_by(username = form.username.data).scalar():
        return render_template("registerform.html", form = form, dberrors = ["Tämä käyttäjännimi on jo käytössä"])

    user = User(form.username.data, pw_hash(form.username.data, form.password.data))
    db.session().add(user)
    db.session().commit()
    login_user(user)
    return redirect(url_for("index"))
    
