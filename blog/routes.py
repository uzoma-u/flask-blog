from flask import render_template, url_for, request, redirect, flash
from blog import app, db
from blog.models import User, Post, Comment, Like
from blog.forms import RegistrationForm, LoginForm, CommentForm, SearchForm
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import desc, asc


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.order_by(Post.date.desc()).limit(3).all()
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/myaccount", methods=["GET", "POST"])
def myaccount():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash("You have succssfully logged in")
            return redirect(url_for("home"))
        else:
            flash("Unsuccessful, kindly check your details")
    return render_template("myaccount.html", title="Login", form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Successful! Thanks for registering")
        login_user(user)
        return redirect(url_for("home"))

        flash("Registration unsuccessful, kindly check your details")

    return render_template("register.html", title="Register", form=form)



@app.route("/post")
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter(Comment.post_id==post.id)
    form = CommentForm()
    return render_template("post.html", post=post, comments=comments, form=form)


@app.route("/post/<int:post_id>/comment", methods=["GET", "POST"])
@login_required
def post_comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        db.session.add(Comment(content=form.comment.data, post_id=post.id, author_id=current_user.id))
        db.session.commit()
        flash("Your comment has been added to the post", "success")
        return redirect(f"/post/{post.id}")
    else:
        flash("Log in to comment")

    comments = Comment.query.filter(Comment.post_id == post.id)
    return render_template("post.html", post=post, comments=comments, form=form)


@app.route("/like/<int:post_id>")
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()

    current_user.like(post)
    db.session.commit()
    flash("You have now liked the post")
    return redirect(f"/post/{post.id}")
    return render_template("post.html", like=like, post=post, form=form, user=user)



@app.route("/unlike/<int:post_id>")
@login_required
def unlike(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    current_user.unlike(post)
    db.session.commit()
    flash("You have have unliked the post")
    return redirect(f"/post/{post.id}")
    return render_template("post.html", unlike=unlike, post=post, form=form, user=user)


@app.route("/search_result", methods=["GET"])
def search_result():
    search = request.args.get("search")
    if search:
        posts = Post.query.filter( Post.title.contains(search) ).all()
        return render_template("search_result.html", posts=posts, search=search)


@app.route("/allposts", methods=["GET", "POST"])
def allposts():
    posts = Post.query.all()

    sortBy = request.args.get("sort")
    if sortBy == "desc":
        posts = Post.query.order_by(Post.date.desc()).all()
        return render_template("allposts.html", posts=posts, sortBy=sortBy)
    else:
        posts = Post.query.order_by(Post.date.asc()).all()
        return render_template("allposts.html", posts=posts)

    return render_template("allposts.html", posts=posts)


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")



@app.route("/logout")
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("home"))


@app.errorhandler(401)
def restricted_page(error):
    return render_template("401.html"), 401

@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template("500.html"), 500

@app.errorhandler(404)
def internal_server_error(error):
    return render_template("404.html"), 404
