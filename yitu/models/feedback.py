# -*- coding: utf-8 -*-
"""
 Created by TyanBoot on 2017/3/30
 Tyan <tyanboot@outlook.com> | <b@duandianer.com>
 一图反馈
"""

from yitu import db


class FeedBackModel(db.Model):
    __tablename__ = "yitu-feedback"
    id_ = db.Column(db.BigInteger, primary_key=True)

    user_id = db.Column(db.Integer)

    contact = db.Column(db.Text)

    date = db.Column(db.DateTime)

    content = db.Column(db.Text)
