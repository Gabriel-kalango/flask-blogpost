from datetime import datetime
from db import db
class Comment(db.Model):
    __tablename__="comment"
    id=db.Column(db.Integer,primary_key=True)
    
    content=db.Column(db.Text,nullable=False)
    author=db.Column(db.String(20),nullable=False,default="N/A")
    date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    user_id= db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False
    )
    user = db.relationship("User")
    post_id=db.Column(db.Integer,db.ForeignKey("blog post.id"),nullable=False)
    blog=db.relationship("BlogPost")