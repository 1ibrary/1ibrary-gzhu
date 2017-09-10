"""
Author: petalsofcherry <1246000821@qq.com>
Date: 2017/6/18
Update By Airing on 2017/9/10
Airing <airing@ursb.me>
"""

# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from yitu.services.gzhu.book_details import BookDetails


class NcuSearch(object):
    def __init__(self):
        self.url = "http://lib.gzhu.edu.cn:8080/bookle/?query={0}&matchesPerPage=10&displayPages=15&index=default&searchPage={1}"

    def get(self, search_text, page=1):
        url = self.url.format(search_text, page)
        data = requests.get(url)
        data.encoding = "utf-8"
        soup = BeautifulSoup(data.text, "lxml")
        tbody = soup.select("div#search_lists")[0]
        books_tr = tbody.find_all("div")[0:]

        books_title = [b.find("a") for b in books_tr]
        # books_author = [b.find("span") for b in books_tr]
        books_info = [{
            "uid": b.attrs["href"].replace('/bookle/search2/detail/', '').replace('?index=default&source=biblios', ''),
            "book_title": b.text.strip(),
        }
            for b in books_title]
        book_details = BookDetails()
        for book_info in books_info:
            book_info.update(book_details.get_details(book_info["uid"]))
            yield book_info


if __name__ == "__main__":
    h = NcuSearch()
    for book_info in h.get("matlab"):
        print(book_info)
