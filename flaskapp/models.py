from email.policy import default
from flaskapp import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model,UserMixin):
    __tablename__='user'
    username=db.Column(db.String(100))
    email=db.Column(db.String(100))
    image_file=db.Column(db.String(100),default="default.jpg")
    password=db.Column(db.String(100))
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    posts=db.relationship('Post',backref='author' ,lazy=True)

class Post(db.Model):
    __tablename__='post'
    postid=db.Column(db.Integer,autoincrement=True,primary_key=True)
    postname=db.Column(db.String(100))
    postdata=db.Column(db.Text)
    date_posted=db.Column(db.DateTime,default=datetime.utcnow())
    userid=db.Column(db.Integer,db.ForeignKey('user.id'))


