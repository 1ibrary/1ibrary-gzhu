# -*- coding: utf-8 -*-
"""
 Created by TyanBoot on 2017/3/30
 Tyan <tyanboot@outlook.com>
 Update By Airing on 2017/9/10
 Airing <airing@ursb.me>
 热门搜索
"""

from yitu import db
import requests
from bs4 import BeautifulSoup
from yitu.models.hot_search import HotSearch as HSModel


class HotSearch(object):
    def __init__(self):
        self.url = "http://lib.gzhu.edu.cn:8080/bookle/"

    def get(self):
        data = requests.get(self.url)
        data.encoding = "utf-8"

        soup = BeautifulSoup(data.text, "lxml")
        top_ten = soup.select("div#hotWordLinks > a")
        top_ten = [i.text for i in top_ten]

        db.session.execute("delete from hot_search")
        keywords = []
        for item in top_ten:
            hs = HSModel(name=item)
            keywords.append(hs)

        db.session.add_all(keywords)
        db.session.commit()
        return top_ten
