from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from application import app, db
from application.models import Post
from application.forms import *
from flask.json import jsonify
from sqlalchemy.sql import text

@app.route("/", methods=["POST"])
@login_required
def posts_create():
    parent = Post.query.filter_by(id=int(request.form.get("parent_msg"))).first()
    parent_id = None
    if parent is not None:
        parent_id = parent.id

    post = Post(request.form.get("message"), parent_id, current_user.id)
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
