from db import db 
from datetime import datetime
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
    comment=db.relationship("Comment",back_populates="blog")
   

    def __repr__(self):
        return f"blogpost {self.id}"
