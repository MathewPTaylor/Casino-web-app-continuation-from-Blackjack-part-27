from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from casinoapp.models import User
from casinoapp import app


class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField("Email", validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired()])

    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField("Sign Up")

    def validate_username(self, username):  # verifying usernam
        user = User.query.filter_by(
            username=username.data).first()  # does a query on the database on any records with the username that the user is trying to use. Returns a User object if a record has the username that the user is trying to use, returns None if no record is found with that username
        if user:
            raise ValidationError("This username already exists.") # Please choose another one.")

    def validate_email(self, email):  # verifying email
        user = User.query.filter_by(
            email=email.data).first()  # same query as the username validation but just with the email field

        if user:  # there is a user that already has that email
            raise ValidationError("An account with this email already exists.")#. Please use another email.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired()])

    submit = SubmitField("Login")

    remember = BooleanField("Remember Me?")


class ForgotPasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")


'''
class ResetPasswordForm(FlaskForm):
  new_password = PasswordField("New Password", validators=[DataRequired()])
  submit = SubmitField("Change Password")
'''