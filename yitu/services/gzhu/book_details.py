"""
Author: Tyan boot <tyanboot@outlook.com>
Date: 2017/6/18
Update By Airing on 2017/9/10
Airing <airing@ursb.me>
获取书籍的详细信息包括馆藏
"""

# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re


class BookDetails(object):
    def __init__(self):
        self.url = "http://lib.gzhu.edu.cn:8080/bookle/search2/detail/{0}?index=default&source=biblios"
        pass

    def get_details(self, uid):
        url = self.url.format(uid)

        data = requests.get(url)
        data.encoding = "utf-8"

        soup = BeautifulSoup(data.text, "lxml")

        isbn_pattern = re.compile('douban.com/isbn/(.*?)/', re.S)
        try:
            isbn = re.findall(isbn_pattern, data.text)
            book_key = isbn[0] if isbn else None
            book_key = book_key.replace("-", "")
        except Exception as e:
            book_key = None

        info = soup.select_one("table.book_holding")
        info_tr = [b.find_all("td") for b in info.find_all("tr")[1:]]

        detail_of_books = [
            dict(zip(("detail_key", "detail_place", "is_borrowed"),
                     [a.text.strip().replace('\r\n                            \r\n                            [架位]','') for a in [b[0]] + [b[4]] + [b[1]]]
                     )
                 )
            for b in info_tr]
        id_ = 1
        for the_book in detail_of_books:
            the_book["detail_id"] = id_
            id_ = id_ + 1
            if the_book["is_borrowed"][:2] == '借出':
                the_book["is_borrowed"] = 1
            else:
                the_book["is_borrowed"] = 0

        return {
            "data": detail_of_books,
            "book_key": book_key,
        }
