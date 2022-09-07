from datetime import datetime
from app.extensions import db
from flask_login import UserMixin

# Subtasks
# Users - Id, username, mail, password, sex, flask coin=100, privacy (public, private, followers)
# Likes - Id, Post id, User id, like date, like status (active, disabled)
# Posts - Id , user id, post text, post image, likers, post type(normal, anonym, VIP)
# Follows - Id, following to id, following from id,  following status (active, disabled) 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    user_image = db.Column(db.String(80), default='static/pfp/default.png')
    flask_coin = db.Column(db.Integer, default=100)
    privacy = db.Column(db.String(50), default='public')
    posts = db.relationship('Post', backref='user', lazy=True, cascade="all, delete-orphan")
    followers = db.relationship('Follow', foreign_keys='Follow.following_to_id', backref='following_to', lazy='dynamic', cascade="all, delete-orphan")
    following = db.relationship('Follow', foreign_keys='Follow.following_from_id', backref='following_from', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f"Username {self.username}', '{self.email}')"
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'flask_coin': self.flask_coin
        }
    
    @classmethod
    def get_user(cls, user_id):
        return cls.query.filter_by(id=user_id).first()
    
    def create(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # check password method
    def check_password(self, password):
        return self.password == password


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_text = db.Column(db.String(200), nullable=False)
    post_image = db.Column(db.String(100))
    post_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    likers = db.relationship('Like', backref='post', lazy=True, cascade='all, delete-orphan')
    post_type = db.Column(db.String(50), default='normal')
    
    def __repr__(self):
        return f"Post('{self.user_id}', '{self.post_text}', '{self.post_image}')"
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_text': self.post_text,
            'post_image': self.post_image,
            'post_date': self.post_date,
            'post_type': self.post_type,
            'likers': self.likers
        }
    
    @classmethod
    def get_post(cls, post_id):
        return cls.query.filter_by(id=post_id).first()
    
    # check if object have image
    @property
    def has_image(self):
        return self.post_image != ''
    
    def create(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    like_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    like_status = db.Column(db.String(10), nullable=False, default='active')

    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'like_date': self.like_date,
            'like_status': self.like_status
        }
    
    @classmethod
    def get_like(cls, like_id):
        return cls.query.filter_by(id=like_id).first()
    
    
    def create(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    following_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    following_from_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    following_status = db.Column(db.String(10), nullable=False, default='active')

    def __repr__(self):
        return f"Follow('{self.following_to_id}', '{self.following_from_id}', '{self.following_status}')"
    
    def __init__(self, following_to_id, following_from_id):
        self.following_to_id = following_to_id
        self.following_from_id = following_from_id
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'following_to_id': self.following_to_id,
            'following_from_id': self.following_from_id,
            'following_status': self.following_status
        }
    
    @classmethod
    def get_follow_by_id(cls, follow_id):
        return cls.query.filter_by(id=follow_id).first()
    
    @classmethod
    def get_by_following_from(cls, following_from_id):
        return cls.query.filter_by(following_from_id=following_from_id).all()
    
    @classmethod
    def get_by_following_to(cls, following_to_id):
        return cls.query.filter_by(following_to_id=following_to_id).all()
    
    @classmethod
    def get_by_both(cls, following_to_id, following_from_id):
        return cls.query.filter_by(following_to_id=following_to_id, following_from_id=following_from_id).first()
    
    def create(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()