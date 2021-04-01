from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment


app = Flask(__name__)
app.config["SECRET_KEY"] = ""
app.config["SQLALCHEMY_DATABASE_URI"] = ""
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
moment = Moment(app)
login_manager = LoginManager()
login_manager.init_app(app)


from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from blog.models import User, Post, Comment
from blog.views import AdminView

admin = Admin(app, name="Admin panel", template_mode="bootstrap3")
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Post, db.session))
admin.add_view(AdminView(Comment, db.session))


from blog import routes
