# -*- coding: utf-8 -*-
"""
 Created by TyanBoot on 2017/3/30
 Tyan <tyanboot@outlook.com>
 热门搜索
"""
from datetime import datetime

from yitu import db


class HotSearch(db.Model):
    __tablename__ = "hot_search"
    id_ = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)
