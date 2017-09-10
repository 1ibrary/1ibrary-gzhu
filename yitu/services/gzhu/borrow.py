# -*- coding: utf-8 -*-
"""
 Created by TyanBoot on 2017/3/30
 Tyan <tyanboot@outlook.com>
 借阅的书
"""

from json import loads

import requests
from bs4 import BeautifulSoup
from flask import g

from yitu.services.douban import Douban
from yitu.services.gzhu.book_details import BookDetails


class Borrowed(object):
    def __init__(self):
        self.session = {
            "PHPSESSID": g.session_id
        }

        self.borrowed_url = "http://210.35.251.243/reader/book_lst.php"

    def get(self):
        data = requests.get(self.borrowed_url, cookies=self.session)
        data.encoding = "utf-8"
        soup = BeautifulSoup(data.text, "lxml")
        books_tr = soup.select("table.table_line > tr")[1:]
        bd = BookDetails()
        db = Douban()
        books = []

        for item in books_tr:
            c = item.find_all("td")
            title = c[1].text
            borrow_time = c[2].text
            return_time = c[3].text
            book_number = c[1].a.attrs["href"][-10:]  # 图书馆内id
            isbn = bd.get_details(book_number)["book_key"]  # isbn
            details = db.search_by_isbn(isbn)  # 详细信息
            if not details:
                continue
            details["book_author"] = loads(details["book_author"])
            details["book_title"] = title
            details["borrow_time"] = borrow_time
            details["return_time"] = return_time
            books.append(details)

        return books
