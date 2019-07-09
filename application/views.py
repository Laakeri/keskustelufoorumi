from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from application import app, db
from application.models import Post
from application.auth.models import User
from application.forms import *
from flask.json import jsonify
from sqlalchemy.sql import text
import urllib.parse

@app.route("/addpost", methods=["POST"])
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

    if request.form.get("redi"):
        return redirect(url_for("thread", pid=int(request.form.get("redi"))))

    return redirect(url_for("index"))

@app.route("/deletepost", methods=["POST"])
@login_required
def delete_post():
    id=int(request.form.get("id"))
    stmt = text("DELETE FROM Post WHERE id = :id AND user_id = :user_id").params(id = id, user_id = current_user.id)
    db.engine.execute(stmt)
    return ""

@app.route("/editpost", methods=["POST"])
@login_required
def edit_post():
    form = PostForm(request.form)
    if not form.validate():
        return redirect(url_for("index"))
    id=int(request.form.get("id"))

    stmt = text("UPDATE Post SET message = :message WHERE id = :id AND user_id = :user_id").params(message = form.message.data, id = id, user_id = current_user.id)
    db.engine.execute(stmt)
    return redirect(url_for("index"))

@app.route("/")
def index():
    return render_template("index.html", postform = PostForm())

@app.route("/thread", methods=["GET"])
def thread():
    post_id=int(request.args.get("pid"))
    post = Post.query.filter_by(id=post_id).first()
    print(post_id)
    print(post.id)
    if post is None:
        return redirect(url_for("index"))
    return render_template("thread.html", post = post, postform = PostForm())

@app.route("/register")
def register():
    return render_template("register.html", form = RegisterForm())

@app.route("/register", methods=["POST"])
def new_user():
    return index()

posts_limit = 4

@app.route("/getposts", methods=["GET"])
def give_posts():
    parent_id = int(request.args.get("parent"))
    offset = int(request.args.get("offset"))
    stmt = text("SELECT Post.message, Post.id, Post.created_at, Account.username, (SELECT COUNT(*) FROM Post Child WHERE Child.parent_id = Post.id) FROM Post Post INNER JOIN Account ON Account.id = Post.user_id WHERE Post.parent_id " + ("IS NULL" if parent_id == 0 else "= :parent_id") + " ORDER BY Post.created_at DESC LIMIT :posts_limit OFFSET :offset").params(parent_id = parent_id, posts_limit = posts_limit+1, offset = offset)
    rows = db.engine.execute(stmt)
    
    response = []
    for row in rows:
        response.append({"message":row[0], "id":row[1], "created_at":row[2], "username":row[3], "children":row[4]})

    next_offset = -1
    if len(response) > posts_limit:
        assert len(response) == posts_limit+1
        next_offset = offset + posts_limit
        limit_reached = True
        response.pop()

    return jsonify({"posts":response, "next_offset":next_offset})

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