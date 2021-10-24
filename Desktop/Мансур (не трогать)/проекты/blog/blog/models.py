from datetime import datetime
from blog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(50), nullable=False) #название поста//до 50 символов
    content = db.Column(db.String(), nullable=False)
    date_posted = db.Column(
        db.DateTime(), nullable=False, default=datetime.now)
    image = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)    
    

    def __repr__(self) -> str:
        return self.title     

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False) #Имя ///до 50 символов
    subject = db.Column(db.String(50), nullable=False) #Объект//до 50 символов
    email = db.Column(db.String(), nullable=False) #email 
    date_posted = db.Column(
        db.DateTime(), nullable=False, default=datetime.now) #дата комментария
    message = db.Column(db.String(), nullable=False) #само сообщение
    post_id = db.Column(db.Integer(), db.ForeignKey(
        'posts.id'), nullable=False) #создаем связь

    def __repr__(self) -> str:
        return self.subject 

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column (db.Integer(), primary_key=True)
    email = db.Column (db.String(), nullable = False, unique = True)
    password = db.Column (db.String(), nullable = False)
    IsAdmin = db.Column (db.Boolean, default = False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self) -> str:
        return self.email