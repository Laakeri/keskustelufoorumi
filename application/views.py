from flask import render_template, request
from application import app, db
from application.models import Post

@app.route("/", methods=["POST"])
def posts_create():
    post = Post(request.form.get("message"), 0)
    db.session().add(post)
    db.session().commit()
    return index()

@app.route("/")
def index():
    return render_template("index.html", posts = Post.query.order_by(Post.created_at.desc()).all())
