from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError, Regexp, InputRequired
from blog.models import User

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=15, message="Username must have more than 3 characters")])
    email = StringField("Email", validators=[DataRequired(), Email()])
    firstname = StringField("Firstname", validators=[DataRequired()])
    lastname = StringField("Lastname", validators=[DataRequired()])
    password = PasswordField("Password (8 or more character)", validators=[DataRequired(), Regexp("^(?=.{8,30})(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^!&*+=])(?=.*[0-9]).*$", message="Your password should have: 1 Uppercase, 1 number, 1 Special character")])
    confirm_password = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password", message="Password must match")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exist. Please choose a different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("User already exist.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")



class CommentForm(FlaskForm):
    comment = StringField("", validators=[InputRequired()])
    submit = SubmitField("Post comment")


class SearchForm(FlaskForm):

    search = StringField("Search", validators=[DataRequired()])
    submit = SubmitField("Search")
