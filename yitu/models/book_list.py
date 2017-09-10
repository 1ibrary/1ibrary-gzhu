"""
Author: Tyan boot <tyanboot@outlook.com>
Date: 2017/6/23
书单
"""

# -*- coding: utf-8 -*-


from yitu import db

BookListR = db.Table("booklist_r",
                     db.Column("list_id", db.Integer, db.ForeignKey("book_lists.id_")),
                     db.Column("book_id", db.Integer, db.ForeignKey("books.book_id")))


class BookList(db.Model):
    __tablename__ = "book_lists"

    id_ = db.Column(db.Integer, primary_key=True)
    # 描述
    description = db.Column(db.Text)
    # 标题
    title = db.Column(db.Text)
    # 所属用户id
    user_id = db.Column(db.Integer, db.ForeignKey("users.id_"), index=True)

    books = db.relationship("Book",
                            secondary=BookListR,
                            backref="book_list")
