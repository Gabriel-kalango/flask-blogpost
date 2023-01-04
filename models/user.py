from db import db
from flask_login import UserMixin
class User(db.Model,UserMixin):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String(200),nullable=False,unique=False)
    lastname=db.Column(db.String(200),nullable=False,unique=False)
    username=db.Column(db.String(200),nullable=False,unique=True)
    email=db.Column(db.String(200),nullable=False,unique=True)
    password_hash=db.Column(db.Text,nullable=False)
    
    posts = db.relationship("BlogPost", back_populates="user",lazy="dynamic")
    comments=db.relationship("Comment",back_populates="user",lazy="dynamic")

    def __repr__(self):
        return f"<user {self.username}>" 