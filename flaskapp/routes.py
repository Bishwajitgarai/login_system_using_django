from flask import render_template,url_for,flash,redirect,request
from flaskapp import app,db,bcrypt
from flaskapp.forms import Registration,Login,Updateaccount,PostCreate,PostUpdate
from flaskapp.models import User,Post
from flask_login import login_user,current_user,logout_user,login_required
from datetime import datetime


@app.route("/home",methods=['GET'])
def home():
    if current_user.is_authenticated:
        # print(current_user)
        allpost=Post.query.filter_by(userid=current_user.id).all()

        return render_template("home.html",title="Home", posts=allpost)
    return render_template("home.html",title="Home")

@app.route("/",methods=['GET','POST'])
def register():
    form=Registration()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        hase_pass=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hase_pass)
        db.session.add(user)
        db.session.commit()
        flash(f"Account Created for {form.username.data}!")
        return redirect(url_for('login'))

    return render_template("register.html",title="register",form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    form=Login()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next=request.args.get("next")
            return redirect(next) if next else redirect(url_for('home'))
        else:

            flash(f"login unucessfull for {form.email.data}! Plesae check email or password")
        
    return render_template("login.html",title="login",form=form)


@app.route('/logout')

def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    form=Updateaccount()
    image_add=url_for("static",filename='profile_pic'+current_user.image_file)
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash("Account details has been updated!")
        return redirect(url_for('account'))
    return render_template('account.html',title="Account",image_file=image_add,form=form)

@app.route("/addpost",methods=['GET','POST'])
@login_required
def addpost():
    form=PostCreate()
    if form.validate_on_submit():
        post=Post(postname=form.postname.data,postdata=form.postdata.data,userid=current_user.id,date_posted=datetime.utcnow())
        db.session.add(post)
        db.session.commit()
        flash("Post Published Succesfully")
        return redirect(url_for('home'))
    return render_template('addpost.html',title="Add Post",form=form)

@app.route("/deletepost/<int:postid>/<int:userid>",methods=['GET','POST'])     
@login_required
def delete_post(postid,userid):
    if userid==current_user.id:
        post=Post.query.filter_by(postid=postid,userid=current_user.id).first()
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        flash("You have no rights to delete the post")
    return redirect(url_for('home'))

@app.route("/updatepost/<int:postid>/<int:userid>",methods=['GET','POST'])     
@login_required
def update_post(postid,userid):
    if userid==current_user.id:
        post=Post.query.filter_by(postid=postid,userid=current_user.id).first()
        form=PostUpdate()
        if form.validate_on_submit():
            post.postname=form.postname.data
            post.postdata=form.postdata.data
            db.session.commit()
            return redirect(url_for('home'))
        form.postname.data=post.postname
        form.postdata.data=post.postdata
        
        return render_template('postedit.html',title="Edit Post",form=form)
    else:
        flash("You have no rights to delete the post")
    return redirect(url_for('home'))





