from db import db
from flask import redirect,render_template,request,url_for,flash
from models import User,Comment
from flask_login import login_required,current_user
from models import BlogPost

from flask_smorest import Blueprint
blb=Blueprint("blog",__name__,description="blogpost endpoint")
@blb.route("/")
def home():
    return render_template("index.html")
@blb.route("/posts", methods=["GET","POST"])

def post():
    
    
        all_post=BlogPost.query.all()

        return render_template("post.html",posts=all_post)
@blb.route("/posts/delete/<int:id>")
@login_required
def delete(id):
    post=BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("blog.post"))
@blb.route("/posts/edit/<int:id>" ,methods=["GET",'POST'])
@login_required
def edit(id):
    post=BlogPost.query.get_or_404(id)
    if request.method=='POST':
        post.title=request.form["title"]
        post.content=request.form["content"]
        post.author=request.form["author"]
        db.session.commit()
        return redirect(url_for("blog.post"))
    else:
        return render_template("edit.html",post=post)

@blb.route("/post/newpost",methods=["GET","POST"])
@login_required
def new_post():
    allpost=User.query.get_or_404(current_user.id)
    if request.method=="POST":
        post_title=request.form["title"]
        post_content=request.form["content"]
        post_author=request.form["author"]
        db.session.add(BlogPost(title=post_title,content=post_content,author=post_author, user_id=current_user.id))
        db.session.commit()
        return redirect(url_for("blog.post")) 
    else:
        return render_template("cud.html",posts=allpost)
@blb.route("/about")
def about():
    return render_template("about.html")
@blb.route("/contact")
def contact():
    return render_template("contact.html")

@blb.route("/post/comment/<int:id>" ,methods=["GET","POST"])
@login_required
def postcomment(id):
    post=BlogPost.query.filter(BlogPost.id==id).first()
    if request.method=="POST":
        post_comment=request.form["comment"]
        comment_add=Comment(content=post_comment,author=current_user.username,user_id=current_user.id,post_id=post.id)
        db.session.add(comment_add)
        db.session.commit()
        flash("comment successful",category="success")
        return redirect(url_for("blog.post"))
    flash("something is wrong",category="danger")
    return render_template("post.html")
    
@blb.route("/post/<int:id>/comments")
@login_required
def postcomments(id):
    posts=BlogPost.query.get(id)
    if not posts:
        flash("no comment posted",category="primary")
        return redirect(url_for("blog.post"))   
    return render_template("comment.html",posts=posts)


