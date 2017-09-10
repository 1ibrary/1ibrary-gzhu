"""
Author: Tyan boot <tyanboot@outlook.com>
Date: 2017/6/20

"""

# -*- coding: utf-8 -*-

from itsdangerous import TimedJSONWebSignatureSerializer

from yitu import db
from yitu.models.book_list import BookList
from yitu.models.subscribe import Subscribe
from flask import g


class User(db.Model):
    __tablename__ = "users"

    id_ = db.Column(db.Integer, primary_key=True)

    xh = db.Column(db.String(10), unique=True, index=True)

    name = db.Column(db.Text)

    password_hash = db.Column(db.Text)

    subscribing = db.relationship('Subscribe',
                                  foreign_keys=[Subscribe.user_id],
                                  backref=db.backref('user', lazy='joined'))

    book_lists = db.relationship("BookList",
                                 foreign_keys=BookList.user_id,
                                 backref=db.backref('user', lazy='joined'))

    @staticmethod
    def verify_token(token):
        from flask import current_app
        expire_time = current_app.config.get("EXPIRES_TIME") or 3600
        token_key = current_app.config["APP_KEY"]

        s = TimedJSONWebSignatureSerializer(token_key, expires_in=expire_time)

        try:
            d = s.loads(token)
            user = User.query.get(d["uid"])
            g.session_id = d["session"]
            return user
        except:
            return None

    @property
    def password(self):
        return None

    @password.setter
    def password(self, pwd):
        import hashlib
        s = hashlib.sha1()
        s.update(pwd.encode("ascii"))
        self.password_hash = s.hexdigest()

    def verify_password(self, pwd):
        import hashlib
        s = hashlib.sha1()
        s.update(pwd.encode("ascii"))
        if s.hexdigest() != self.password_hash:
            return False
        else:
            return True

    def generate_token(self, session):
        from flask import current_app
        expire_time = current_app.config.get("EXPIRES_TIME") or 3600
        token_key = current_app.config["APP_KEY"]

        s = TimedJSONWebSignatureSerializer(token_key, expires_in=expire_time)
        d = s.dumps({"username": self.xh, "uid": self.id_, "session": session})
        return d.decode("ascii")
