from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from application import app, db
from application.models import Post
from application.auth.models import User
from application.forms import *
from flask.json import jsonify
from sqlalchemy.sql import text
import urllib.parse

@app.route("/", methods=["POST"])
@login_required
def posts_create():
    form = PostForm(request.form)
    if not form.validate():
        return redirect(url_for("index"))

    parent = Post.query.filter_by(id=int(request.form.get("parent_msg"))).first()
    parent_id = None
    if parent is not None:
        parent_id = parent.id

    post = Post(form.message.data, parent_id, current_user.id)
    db.session().add(post)
    db.session().commit()
    return redirect(url_for("index"))

@app.route("/")
def index():
    return render_template("index.html", postform = PostForm())

@app.route("/register")
def register():
    return render_template("register.html", form = RegisterForm())

@app.route("/register", methods=["POST"])
def new_user():
    return index()

@app.route("/getposts", methods=["GET"])
def give_posts():
    parent_id = int(request.args.get("parent"))
    stmt = text("SELECT Post.message, Post.id, Post.created_at, Account.username, (SELECT COUNT(*) FROM Post Child WHERE Child.parent_id = Post.id) FROM Post Post INNER JOIN Account ON Account.id = Post.user_id WHERE Post.parent_id " + ("IS NULL" if parent_id == 0 else "= :parent_id") + " ORDER BY Post.created_at DESC").params(parent_id = parent_id)
    rows = db.engine.execute(stmt)
    #posts = Post.query.filter_by(parent_id = request.args.get("parent")).order_by(Post.created_at.desc()).all()
    response = []
    for row in rows:
        response.append({"message":row[0], "id":row[1], "created_at":row[2], "username":row[3], "children":row[4]})
    return jsonify(response)

@app.route("/profile", methods=["GET"])
def profile():
    user = User.query.filter_by(username=request.args.get("user")).first()
    postcount = 0
    errors = []
    if user is None:
        errors = ["Käyttäjää ei ole olemassa"]
    else:
        postcount = Post.query.filter_by(user_id=user.id).count()
    return render_template("profile.html", user=user, errors=errors, postcount=postcount, descform = DescForm())

def own_profile():
    return redirect(url_for("profile")+"?user="+urllib.parse.quote(current_user.username))

@app.route("/change_desc", methods=["POST"])
def change_desc():
    form = DescForm(request.form)

    if not form.validate():
        return own_profile()

    if current_user.is_authenticated:
        current_user.description = form.description.data
        db.session.commit()
    return own_profile()