from blog import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



class Like(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    liker_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    liked_post = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Like('{self.id}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(40), nullable=False, default="default.jpg")
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    likers = db.relationship("Like", foreign_keys=[Like.liked_post], backref=db.backref("post", lazy="joined"), lazy="dynamic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Post('{self.date}', '{self.title}', '{self.content}')"


    def is_liked_by(self, user):
        if user.id is None:
            return False
        return self.likers.filter_by(liker_id=user.id).first() is not None


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    firstname = db.Column(db.String(120), unique=False, nullable=False)
    lastname = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship("Post", backref="user", lazy=True)
    comment = db.relationship("Comment", backref="user", lazy=True)
    liked = db.relationship("Like", foreign_keys=[Like.liker_id], backref=db.backref("user", lazy="joined"), lazy="dynamic", cascade="all, delete-orphan")
    is_admin = db.Column(db.Boolean, nullable=False, default=False)


    def __repr__(self):
        return f"User('{self.username}', '{self.firstname}', '{self.lastname}', '{self.email}')"

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def like(self, post):
        if not self.is_liking(post):
            likes = Like(liker_id=self.id, liked_post=post.id)
            db.session.add(likes)

    def unlike(self, post):
        likes = self.liked.filter_by(liked_post=post.id).first()
        if likes:
            db.session.delete(likes)

    def is_liking(self, post):
        if Post.id is None:
            return False
        return self.liked.filter_by(liked_post=post.id).first() is not None


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("comment.id"), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    parent = db.relationship("Comment", backref="comment_parent", remote_side=id, lazy=True)

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date}')"
