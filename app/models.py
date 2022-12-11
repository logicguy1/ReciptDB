from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login

from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Integer, default=lambda: 0)
    recipts = db.relationship('Recipt', backref='author', lazy='dynamic')
    tags = db.relationship('UserTag', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.admin == 1

    def __repr__(self):
        return f'<User {self.email}>'


class UserTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(50))
    color = db.Column(db.String(10))


class Recipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    store = db.Column(db.String(128))
    body = db.Column(db.String(4000))
    timestamp = db.Column(db.String(60))
    img_src = db.Column(db.String(120), unique=True)
    total = db.Column(db.String(120))
    tags = db.relationship('Tag', backref='recipt', lazy='dynamic')

    def __repr__(self):
        return f'<Recipt {self.id}>'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipt_id = db.Column(db.Integer, db.ForeignKey('recipt.id'))
    user_tag_id = db.Column(db.Integer, db.ForeignKey('user_tag.id'))



@login.user_loader
def load_user(id):
    return User.query.get(int(id))
