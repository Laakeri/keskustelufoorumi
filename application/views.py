from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from application import app, db
from application.models import Post
from application.forms import PostForm

@app.route("/", methods=["POST"])
@login_required
def posts_create():
    post = Post(request.form.get("message"), 0, current_user.id)
    db.session().add(post)
    db.session().commit()
    return redirect(url_for("index"))

@app.route("/")
def index():
    return render_template("index.html", posts = Post.query.order_by(Post.created_at.desc()).all(), postform = PostForm())

@app.route("/register")
def register():
    return render_template("register.html", form = RegisterForm())

@app.route("/register", methods=["POST"])
def new_user():
    return index()
