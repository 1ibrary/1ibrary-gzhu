# -*- coding: utf-8 -*-


import json

import jpush
from flask_restful import Resource

from yitu import db
from yitu.models.book import Book, HotBook as HBModel
from yitu.models.hot_search import HotSearch as HSModel
from yitu.models.user import User
from yitu.services.douban import Douban
from yitu.services.gzhu.library_search import NcuSearch
from yitu.utils import get_request_params


class HotBook(Resource):
    decorators = []

    def post(self):
        args = get_request_params([
            ("page", int, True, "json"),
            ("uid", int, True, "json"),
            ("timestamp", float, True, "json"),
            ("token", str, True, "json")
        ])

        page = args["page"]
        uid = args["uid"]
        timestamp = args["timestamp"]
        token = args["token"]

        user = User.verify_token(token)
        if user is None or user.id_ != uid:
            return {
                "data": [],
                "status": 2,
                "msg": "认证失败"
            }
        try:
            pagination = Book.query.filter_by(is_hot=True) \
                .order_by(Book.hot_id.desc()) \
                .paginate(page, per_page=20, error_out=False).items

            return {
                "status": 0,
                "msg": "搜索成功",
                "data": [{
                    "book_last_number": book.book_last_number,
                    "book_cover": book.book_cover,
                    "book_id": book.book_id,
                    "book_author": json.loads(book.book_author),
                    "book_title": book.book_title,
                    "book_db_id": book.book_db_id,
                    "book_publish": book.book_publish,
                    "book_rate": book.book_rate
                }
                    for book in pagination]
            }
        except Exception as e:
            return {
                "data": [],
                "status": 2,
                "msg": "数据库溜了"
            }


class SearchBook(Resource):
    decorators = []

    def post(self):
        args = get_request_params([
            ("timestamp", float, True, "json"),
            ("token", str, True, "json"),
            ("content", str, True, "json"),
            ("uid", int, True, "json"),
            ("type", int, True, "json"),
            ("page", int, False, "json")
        ])

        timestamp = args["timestamp"]
        token = args["token"]
        content = args["content"]
        uid = args["uid"]
        type = args["type"]

        user = User.verify_token(token)
        if user is None or user.id_ != uid:
            return {
                "data": [],
                "status": 1,
                "msg": "认证失败"
            }

        try:
            clear_content = content
            if type == 0:
                books_of_db = Book.query.filter(Book.book_title.like('%' + clear_content + '%')).paginate(
                    page=args["page"], per_page=20, error_out=False).items
            elif type == 1:
                books_of_db = Book.query.filter(Book.book_author.like('%' + clear_content + '%')).paginate(
                    page=args["page"], per_page=20, error_out=False).items
            else:
                books_of_db = Book.query.filter(Book.book_publish.like('%' + clear_content + '%')).paginate(
                    page=args["page"], per_page=20, error_out=False).items

        except Exception as e:
            return {
                "data": [],
                "status": 2,
                "msg": "数据库溜了"
            }

        if books_of_db:
            return {
                "status": 0,
                "msg": "搜索成功",
                "data": [{
                    "book_cover": book.book_cover,
                    "book_id": book.book_id,
                    "book_rate": book.book_rate,
                    "book_title": book.book_title,
                    "book_author": json.loads(book.book_author),
                    "book_last_number": book.book_last_number,
                    "book_db_id": book.book_db_id,
                    "book_publish": book.book_publish
                } for book in books_of_db]
            }

        else:
            ncu_search = NcuSearch()
            douban = Douban()
            data = []

            try:
                for book_info in ncu_search.get(content, args["page"]):
                    if book_info["book_key"]:
                        b = douban.search_by_isbn(book_info["book_key"])
                        if not b:
                            continue
                        book_info.update(b)

                        b = Book.query.filter_by(book_key=book_info["book_key"]).first()
                        if b:
                            continue
                        new_book = Book(book_author=book_info["book_author"])
                        new_book.book_cover = book_info["book_cover"]
                        new_book.book_rate = book_info["book_rate"]
                        new_book.book_content = book_info["book_content"]
                        new_book.book_publish = book_info["book_publish"]
                        new_book.book_last_number = len(
                            list(filter(lambda x: not x["is_borrowed"], book_info["data"])))
                        new_book.book_key = book_info["book_key"]
                        new_book.book_db_id = book_info["book_db_id"]
                        new_book.book_title = book_info["book_title"]
                        new_book.detail_data = json.dumps(book_info["data"])

                        db.session.add(new_book)
                        db.session.commit()

                        mydict = {
                            "book_cover": book_info["book_cover"],
                            "book_id": new_book.book_id,
                            "book_rate": book_info["book_rate"],
                            "book_title": book_info["book_title"],
                            "book_author": json.loads(book_info["book_author"]),
                            "book_last_number": new_book.book_last_number,
                            "book_db_id": book_info["book_db_id"],
                            "book_publish": book_info["book_publish"]
                        }
                        data.append(mydict)

                    else:
                        b = douban.search_by_isbn(book_info["book_title"])
                        if not b:
                            continue
                        book_info.update(b)

                        b = Book.query.filter_by(book_db_id=book_info["book_db_id"]).first()
                        if b:
                            continue
                        new_book = Book(book_author=book_info["book_author"])
                        new_book.book_cover = book_info["book_cover"]
                        new_book.book_rate = book_info["book_rate"]
                        new_book.book_content = book_info["book_content"]
                        new_book.book_publish = book_info["book_publish"]
                        new_book.book_last_number = len(
                            list(filter(lambda x: not x["is_borrowed"], book_info["data"])))
                        new_book.book_key = book_info["book_key"]
                        new_book.book_db_id = book_info["book_db_id"]
                        new_book.book_title = book_info["book_title"]
                        new_book.detail_data = json.dumps(book_info["data"])

                        db.session.add(new_book)
                        db.session.commit()

                        mydict = {
                            "book_cover": book_info["book_cover"],
                            "book_id": new_book.book_id,
                            "book_rate": book_info["book_rate"],
                            "book_title": book_info["book_title"],
                            "book_author": json.loads(book_info["book_author"]),
                            "book_last_number": new_book.book_last_number,
                            "book_db_id": book_info["book_db_id"],
                            "book_publish": book_info["book_publish"]
                        }
                        data.append(mydict)
                return {
                    "status": 0,
                    "msg": "搜索成功",
                    "data": data
                }
            except Exception as e:
                print(e)
                return {
                    "data": [],
                    "status": 3,
                    "msg": "服务器溜了"
                }


class ShowDetail(Resource):
    decorators = []

    def post(self):
        args = get_request_params([
            ("timestamp", float, True, "json"),
            ("book_db_id", int, True, "json"),
            ("token", str, True, "json"),
            ("book_id", int, True, "json"),
            ("uid", int, True, "json"),
        ])

        timestamp = args["timestamp"]
        book_db_id = args["book_db_id"]
        token = args["token"]
        book_id = args["book_id"]
        uid = args["uid"]

        user = User.verify_token(token)
        if user is None or user.id_ != uid:
            return {
                "data": [],
                "status": 2,
                "msg": "认证失败"
            }
        try:
            the_book = Book.query.filter_by(book_id=book_id).first()
            if not the_book:
                return {
                    "status": 0,
                    "message": "搜索成功",
                    "data": None
                }
            the_detail_data = json.loads(the_book.detail_data)

            return {
                "status": 0,
                "msg": "搜索成功",
                "data": {
                    "book_rate": the_book.book_rate,
                    "book_content": the_book.book_content,
                    "book_publish": the_book.book_publish,
                    "book_last_number": the_book.book_last_number,
                    "book_key": the_book.book_key,
                    "book_db_id": the_book.book_db_id,
                    "book_title": the_book.book_title,
                    "detail_data": the_detail_data,
                    "book_author": json.loads(the_book.book_author),
                    "book_place": None if len(the_detail_data) == 0 else the_detail_data[0]["detail_place"],
                    "book_id": the_book.book_id,
                    "book_cover": the_book.book_cover,
                    "is_subscribe": 1 if uid in the_book.subscribers else 0
                }
            }

        except Exception as e:
            return {
                "data": [],
                "status": 2,
                "msg": "服务器溜了"
            }


class Subscribe_(Resource):
    def post(self):
        args = get_request_params([
            ("timestamp", float, True, "json"),
            ("token", str, True, "json"),
            ("book_id", int, True, "json"),
            ("uid", int, True, "json")
        ])

        timestamp = args["timestamp"]
        token = args["token"]
        book_id = args["book_id"]
        uid = args["uid"]

        def _push_msg(message, device_id):
            app_key = 'app_key'
            master_secret = 'master_key'

            _jpush = jpush.JPush(app_key, master_secret)
            push = _jpush.create_push()
            # push.audience = jpush.audience([{"registration_id":device_id}])
            push.audience = {'registration_id': [device_id]}
            # push.audience = device_id
            android_msg = jpush.android(
                message,
                None,
                None,
                {
                    "msg": message,  # 强行套用app中notification的相关格式
                    "status": 0
                }
            )
            ios_msg = jpush.ios(
                message,
                None,
                None,
                {
                    "msg": message,  # 强行套用app中notification的相关格式
                    "status": 0
                }
            )
            push.notification = jpush.notification("hello jpush", ios_msg, android_msg, None)
            # push.options = {"time_to_live": 86400, "sendno": 12345, "apns_production":True}
            push.options = {"time_to_live": 86400, "apns_production": True}
            push.platform = jpush.platform("all")

            push.send()

        the_book = Book.query.filter_by(book_id=book_id).first()
        the_detail_data = json.loads(the_book.detail_data)
        flag = 0
        for a_book in the_detail_data:
            if a_book["is_borrowed"] == 1:
                flag = 1
        if flag == 1:
            _push_msg("有书了", uid)


class HotSearch(Resource):
    def post(self):
        hs = HSModel.query.all()
        return {
            "status": 0,
            "msg": "获取成功",
            "data": [k.name for k in hs]
        }
