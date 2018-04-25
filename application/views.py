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
    post = Post(request.form.get("message"), request.form.get("parent_msg"), current_user.id)
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
    stmt = text("SELECT Post.message, Post.id, Post.created_at, User.username, count(Child.id) FROM Post Post INNER JOIN User ON User.id = Post.user_id LEFT JOIN Post Child ON Child.parent_id = Post.id WHERE Post.parent_id = :parent_id GROUP BY Post.id ORDER BY Post.created_at DESC").params(parent_id = request.args.get("parent"))
    rows = db.engine.execute(stmt)
    #posts = Post.query.filter_by(parent_id = request.args.get("parent")).order_by(Post.created_at.desc()).all()
    response = []
    for row in rows:
        response.append({"message":row[0], "id":row[1], "created_at":row[2], "username":row[3], "children":row[4]})
    return jsonify(response)
