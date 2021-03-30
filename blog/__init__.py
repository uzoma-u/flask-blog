from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment


app = Flask(__name__)
app.config["SECRET_KEY"] = "d6df90423a90ace08d0e0d81817668adfae7763f100db87e"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://c2067643:Simplicity5409*@csmysql.cs.cf.ac.uk:3306/c2067643_database1"
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
