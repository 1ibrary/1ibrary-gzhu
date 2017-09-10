"""
Author: Tyan boot <tyanboot@outlook.com>
Date: 2017/6/18
获取热门书籍
"""

# -*- coding: utf-8 -*-

import json

import requests
from bs4 import BeautifulSoup

from yitu import db
from yitu.models.book import HotBook, Book
from yitu.services.douban import Douban
from yitu.services.gzhu.book_details import BookDetails


class HotBooks(object):
    def __init__(self):
        self.url = "http://210.35.251.243/top/top_lend.php?cls_no={0}"
        pass

    def get(self, category="ALL"):
        """
        获取热门排行
        :parameter category 分类
        :return: 
        """
        db.session.execute("DELETE FROM hot_books WHERE is_hot=1")

        url = self.url.format(category)
        data = requests.get(url)
        data.encoding = "utf-8"
        soup = BeautifulSoup(data.text, "lxml")
        tbody = soup.find("table")
        books_tr = tbody.find_all("tr")[1:]

        books = [b.find_all("td") for b in books_tr]

        books_info = [{
            "hot_id": int(b[0].text),
            "book_title": b[1].text,
            "book_publish": b[3].text,
            "book_last_number": int(b[5].text) - int(b[6].text),
            "uid": b[1].find("a").attrs["href"][-10:]
        }
            for b in books]

        douban = Douban()
        book_details = BookDetails()
        for book_info in books_info:
            book_info.update(book_details.get_details(book_info["uid"]))
            if book_info["book_key"]:
                b = douban.search_by_isbn(book_info["book_key"])
            else:
                b = douban.search_by_else(book_info["book_title"])

            if not b:
                continue

            book_info.update(b)
            b = Book.query.filter_by(book_db_id=book_info["book_db_id"]).first()
            if not b:
                book = Book(book_author=book_info["book_author"])
                book.book_cover = book_info["book_cover"]
                book.book_rate = book_info["book_rate"]
                book.book_content = book_info["book_content"]
                book.book_publish = book_info["book_publish"]
                book.book_last_number = len(book_info["data"])
                book.book_key = book_info["book_key"]
                book.book_db_id = book_info["book_db_id"]
                book.book_title = book_info["book_title"]
                book.detail_data = json.dumps(book_info["data"])
                book.hot_id = book_info["hot_id"]
                book.book_last_number = book_info["book_last_number"]
                book.is_hot = True
                db.session.add(book)
            db.session.commit()


def task():
    h = HotBooks()
    h.get()
    print("task run")
