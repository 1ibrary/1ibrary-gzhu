# -*- coding: utf-8 -*-

import json

import requests


class Douban(object):
    def __init__(self):
        self.search_by_isbn_url = "https://api.douban.com/v2/book/isbn/{0}"
        self.search_by_else_url = "https://api.douban.com/v2/book/search?q={0}"

    def search_by_isbn(self, isbn):
        isbn = isbn.replace("-", "")

        url = self.search_by_isbn_url.format(isbn)
        data = requests.get(url)
        result = json.loads(data.text)

        if "code" in result:
            return None
        return {
            "book_rate": float(result['rating']['average']),
            "book_db_id": int(result['id']),
            "book_cover": result['image'],
            "book_content": result['summary'],
            "book_author": json.dumps(result['author'])
        }

    def search_by_else(self, query_string):
        url = self.search_by_else_url.format(query_string)
        data = requests.get(url)
        results = json.loads(data.text)
        if "code" in results:
            return None

        if len(results["books"]) == 0:
            return None
        result = results['books'][0]

        return {
            "book_rate": float(result['rating']['average']),
            "book_db_id": int(result['id']),
            "book_cover": result['image'],
            "book_key": result['isbn13'],
            "book_content": result['summary'],
            "book_author": json.dumps(result['author'])
        }
