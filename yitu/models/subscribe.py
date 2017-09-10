from datetime import datetime

from yitu import db


class Subscribe(db.Model):
    __tablename__ = "subscribes"
    id_ = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id_'), index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
