
from flask import Flask
from models import User
from db import db
import os
from resources.user import blp as userblueprint
from resources.blog import blb as blogblueprint
from flask_login import LoginManager

app=Flask(__name__)
base_dir=os.path.dirname(os.path.realpath(__file__))
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(base_dir,"posts.db")
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False
app.config["SECRET_KEY"] = '026b0eb800ec34fb5cf2e7'
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view='login'

db.init_app(app)



with app.app_context():
    db.create_all()
    
@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))

# all_post=[{"title":"Post 1","content":"this is just the beginning"},{"title":"Post 2","content":"this is just the ending"}]


app.register_blueprint(userblueprint)
app.register_blueprint(blogblueprint)
if __name__=="__main__":
    app.run(debug=True)