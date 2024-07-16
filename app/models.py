from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }



class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_blog_user'), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author_id': self.author_id,
            'created_on': self.created_on, 
            'updated_on': self.updated_on 
        }

