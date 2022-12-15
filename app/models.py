from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login
from datetime import datetime
import uuid
import os

from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Integer, default=lambda: 0)

    recipts = db.relationship('Recipt', backref='author', lazy='dynamic')
    tags = db.relationship('UserTag', backref='author', lazy='dynamic')
    code = db.relationship('Invite', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.admin == 1

    def deep_delete(self):
        recipts = self.recipts

        for r in recipts:
            r.tags.delete()

            if r.img_src is not None:
                try:
                    os.remove(f'app/assets/recipts/{r.img_src}') 
                except FileNotFoundError:
                    pass

        self.tags.delete()
        recipts.delete()
            

    def __repr__(self):
        return f'<User {self.email}>'


class Recipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    store = db.Column(db.String(128))
    body = db.Column(db.String(4000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    img_src = db.Column(db.String(120), unique=True)
    total = db.Column(db.Float())
    tags = db.relationship('Tag', backref='recipt', lazy='dynamic')
    share = db.relationship('Share', backref='recipt', lazy='dynamic')

    def get_tags(self):
        tags = self.tags.all()
        tags = [tag.usr_tag for tag in tags]
        return tags

    def get_month(self):
        return self.timestamp.strftime("%Y-%m")

    def get_share_link(self):
        share = self.share.first()
        if share is not None:
            return share.code

        # If the user has no codes create a new one from a hex encoded UUID4
        lnk = uuid.uuid4().hex
        share = Share(code=lnk, recipt_id=self.id)
        db.session.add(share)
        db.session.commit()

        return lnk

    def __repr__(self):
        return f'<Recipt {self.id}>'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipt_id = db.Column(db.Integer, db.ForeignKey('recipt.id'))
    user_tag_id = db.Column(db.Integer, db.ForeignKey('user_tag.id'))


class UserTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(50))
    color = db.Column(db.String(10))
    tags = db.relationship('Tag', backref='usr_tag', lazy='dynamic')


class Invite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100))
    # 0 = avaliable, 1 = taken, 2 = blocked
    status = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Invite {self.code}>"


class Share(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100))
    recipt_id = db.Column(db.Integer, db.ForeignKey('recipt.id'))

    def __repr__(self):
        return f"<Share {self.code}>"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
