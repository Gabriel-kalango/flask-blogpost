from db import db
from flask import redirect,render_template,request,url_for,flash
from models import User
from flask_login import login_user,logout_user,login_required
from werkzeug.security import check_password_hash,generate_password_hash
from flask_smorest import Blueprint
blp=Blueprint("user",__name__,description="user endpoint")
@blp.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        username=request.form["username"]
        email=request.form["email"]
        password_hash=request.form["password"]
        firstname=request.form.get("firstname")
        lastname=request.form.get("lastname")
        user=User.query.filter_by(username=username).first()
        email_check=User.query.filter_by(email=email).first()
        if user:
            flash("username already in use",category="danger")
            return redirect(url_for("user.signup"))
            

        elif email_check:
            flash("emaill already in use", category="danger")
            return redirect(url_for("user.signup"))
        password_hash=generate_password_hash(password_hash)

        
        sign_up_user=User(username=username,email=email,password_hash=password_hash,firstname=firstname,lastname=lastname)
        db.session.add(sign_up_user)
        db.session.commit()
        flash("sign in successful", category="success")
        return redirect(url_for("user.login"))
    return render_template("signup.html")
@blp.route("/login",methods=["GET","POST"]) 
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        user=User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash,password):
            login_user(user)
            flash("welcome",category="success")
            return redirect(url_for("blog.post"))
        else:
            flash("incorrect username or password", category="danger")
    return render_template("login.html")
@blp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("blog.home"))