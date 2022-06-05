from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flaskapp.models import User
from flask_login import current_user



class Registration(FlaskForm):
    username=StringField("Username",validators=[DataRequired(),Length(min=2,max=40)])
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired()])
    confirm_password=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField("Register")

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken . Please chosse other')
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken')

class Login(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired()])
    remember=BooleanField("Remmber Me")
    submit=SubmitField("Log In")

class Updateaccount(FlaskForm):
    username=StringField("Username",validators=[DataRequired(),Length(min=2,max=40)])
    email=StringField("Email",validators=[DataRequired(),Email()])
    submit=SubmitField("Update")

    def validate_username(self,username):
        if username.data!=current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken . Please chosse other')
    def validate_email(self,email):
        if email.data!=current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is taken')

class PostCreate(FlaskForm):
    postname=StringField("Post Titile",validators=[DataRequired(),Length(min=2)])
    postdata=StringField("Post Content",validators=[DataRequired(),Length(min=2)])
    submit=SubmitField("Post")

class PostUpdate(FlaskForm):
    postname=StringField("Post Titile",validators=[DataRequired(),Length(min=2)])
    postdata=StringField("Post Content",validators=[DataRequired(),Length(min=2)])
    submit=SubmitField("Post Update")