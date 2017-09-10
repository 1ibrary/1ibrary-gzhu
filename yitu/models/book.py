# -*- coding: utf-8 -*-

from yitu import db
from yitu.models.subscribe import Subscribe


class Book(db.Model):
    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True)
    book_author = db.Column(db.Text)
    book_cover = db.Column(db.Text)
    book_rate = db.Column(db.Integer)
    book_content = db.Column(db.Text)
    book_publish = db.Column(db.Text)
    book_last_number = db.Column(db.Integer)
    book_key = db.Column(db.String(13), index=True)
    book_db_id = db.Column(db.Integer, unique=True)
    book_title = db.Column(db.Text)
    book_place = db.Column(db.Text)
    detail_data = db.Column(db.Text)

    hot_id = db.Column(db.Integer)

    is_hot = db.Column(db.Boolean, default=False)

    subscribers = db.relationship('Subscribe',
                                  foreign_keys=[Subscribe.book_id],
                                  backref=db.backref('book', lazy='joined'))


class HotBook(db.Model):
    __tablename__ = "hot_books"

    book_id = db.Column(db.Integer, primary_key=True)
    book_author = db.Column(db.Text)
    book_cover = db.Column(db.Text)
    book_rate = db.Column(db.Integer)
    book_content = db.Column(db.Text)
    book_publish = db.Column(db.Text)
    book_last_number = db.Column(db.Integer)
    book_key = db.Column(db.String(13), index=True)
    book_db_id = db.Column(db.Integer, unique=True)
    book_title = db.Column(db.Text)
    book_place = db.Column(db.Text)
    detail_data = db.Column(db.Text)

    hot_id = db.Column(db.Integer)
