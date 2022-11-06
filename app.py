
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import login_user,logout_user,UserMixin,current_user,login_required,LoginManager

app=Flask(__name__)
base_dir=os.path.dirname(os.path.realpath(__file__))
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(base_dir,"posts.db")
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False
app.config["SECRET_KEY"] = '026b0eb800ec34fb5cf2e7'
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view='login'
db=SQLAlchemy(app)
class BlogPost(db.Model):
    __tablename__="blog post"
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    content=db.Column(db.Text,nullable=False)
    author=db.Column(db.String(20),nullable=False,default="N/A")
    date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user_id= db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False
    )
    user = db.relationship("User")


    def __repr__(self):
        return f"blogpost {self.id}"



class User(db.Model,UserMixin):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String(200),nullable=False,unique=False)
    lastname=db.Column(db.String(200),nullable=False,unique=False)
    username=db.Column(db.String(200),nullable=False,unique=True)
    email=db.Column(db.String(200),nullable=False,unique=True)
    password_hash=db.Column(db.Text,nullable=False)
    
    posts = db.relationship("BlogPost", back_populates="user",lazy="dynamic")

    def __repr__(self):
        return f"<user {self.username}>"
with app.app_context():
    db.create_all()
    
@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))

# all_post=[{"title":"Post 1","content":"this is just the beginning"},{"title":"Post 2","content":"this is just the ending"}]
@app.route("/signup",methods=["GET","POST"])
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
            return redirect("/signup")

        if email_check:
            return redirect("/signup")
        password_hash=generate_password_hash(password_hash)

        
        sign_up_user=User(username=username,email=email,password_hash=password_hash,firstname=firstname,lastname=lastname)
        db.session.add(sign_up_user)
        db.session.commit()
        return redirect("/login")
    return render_template("signup.html")
@app.route("/login",methods=["GET","POST"])
def login():
    username=request.form.get("username")
    password=request.form.get("password")
    user=User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash,password):
        login_user(user)
        return redirect("/posts")
    return render_template("login.html")
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/posts", methods=["GET","POST"])

def post():
    
    
        all_post=BlogPost.query.all()

        return render_template("post.html",posts=all_post)
@app.route("/posts/delete/<int:id>")
@login_required
def delete(id):
    post=BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/posts")
@app.route("/posts/edit/<int:id>" ,methods=["GET",'POST'])
@login_required
def edit(id):
    post=BlogPost.query.get_or_404(id)
    if request.method=='POST':
        post.title=request.form["title"]
        post.content=request.form["content"]
        post.author=request.form["author"]
        db.session.commit()
        return redirect("/posts")
    else:
        return render_template("edit.html",post=post)

@app.route("/post/newpost",methods=["GET","POST"])
@login_required
def new_post():
    allpost=User.query.get_or_404(current_user.id)
    if request.method=="POST":
        post_title=request.form["title"]
        post_content=request.form["content"]
        post_author=request.form["author"]
        db.session.add(BlogPost(title=post_title,content=post_content,author=post_author, user_id=current_user.id))
        db.session.commit()
        return redirect("/posts") 
    else:
        return render_template("cud.html",posts=allpost)
@app.route("/about")
def about():
    return render_template("/about.html")
@app.route("/contact")
def contact():
    return render_template("/contact.html")
if __name__=="__main__":
    app.run(debug=True)