# -*- coding: utf-8 -*-


import json
import time
from datetime import datetime

from flask_restful import Resource

from yitu import db
from yitu.models.book import Book, Subscribe as SubModel
from yitu.models.book_list import BookList as BookListModel, BookList
from yitu.models.feedback import FeedBackModel
from yitu.models.user import User
from yitu.services.gzhu.borrow import Borrowed
from yitu.services.gzhu.login import Login as LoginService
from yitu.utils import get_request_params


class Login(Resource):
    def post(self):
        args = get_request_params([
            ("account", str, True, "json"),
            ("password", str, True, "json"),
            ("school_id", int, True, "json")
        ])

        account = args["account"]
        pwd = args["password"]
        school_id = args["school_id"]

        # todo: check for school_id

        u = User.query.filter_by(xh=account).first()

        if not u:
            # 第一次登陆, 先尝试登录学校图书馆
            result, name = LoginService().login(account, pwd)
            if not result:
                return {
                    "status": 1,
                    "msg": "用户名或密码错误"
                }

            u = User(xh=account)
            u.password = pwd
            u.name = name
            try:
                db.session.add(u)
                db.session.commit()
                epoch = int(time.time())
                return {
                    "status": 0,
                    "msg": "注册成功",
                    "data": {
                        "timestamp": epoch,
                        "uid": u.id_,
                        "username": name,
                        "token": u.generate_token(result)
                    }
                }
            except Exception as e:
                return {
                    "status": 2,
                    "msg": "服务器溜了"
                }
            pass

        result, name = LoginService().login(account, pwd)

        if not result:
            return {
                "status": 1,
                "msg": "用户名或密码错误"
            }
        return {
            "status": 0,
            "msg": "登陆成功",
            "data": {
                "timestamp": int(time.time()),
                "uid": u.id_,
                "username": name,
                "token": u.generate_token(result)
            }
        }


class CollectBook(Resource):
    def post(self):
        args = get_request_params([
            ("timestamp", int, True, "json"),
            ("book_id", int, True, "json"),
            ("uid", int, True, "json"),
            ("book_db_id", int, True, "json"),
            ("token", str, True, "json"),
            ("list_id", int, True, "json")
        ])

        book_id = args["book_id"]
        uid = args["uid"]
        token = args["token"]
        list_id = args["list_id"]

        book_list: BookListModel = BookListModel.query.get(list_id)

        user = User.verify_token(token)

        if (not user) or (user.id_ != uid):
            return {
                "status": 1,
                "msg": "没有登录"
            }

        if not book_list:
            return {
                "status": 2,
                "msg": "书单不存在"
            }

        if book_list.user_id != uid:
            return {
                "status": 3,
                "msg": "书单不是你的"
            }

        book = Book.query.get(book_id)
        if not book:
            return {
                "status": 4,
                "msg": "图书不存在"
            }
        book_list.books.append(book)

        try:
            db.session.add(book_list)
            db.session.commit()

            return {
                "status": 0,
                "msg": "添加成功"
            }
        except Exception as e:
            return {
                "status": 5,
                "msg": "服务器炸了"
            }


class ShowList(Resource):
    def post(self):
        """
        获取书单
        :return:
        """
        args = get_request_params([
            ("token", str, True, "json"),
            ("uid", int, True, "json")
        ])

        token = args["token"]
        uid = args["uid"]

        user = User.verify_token(token)

        if (not user) or (user.id_ != uid):
            return {
                "status": 1,
                "msg": "未登录"
            }

        brs = BookListModel.query.filter_by(user_id=uid).all()
        data = [
            {
                "list_id": br.id_,
                "book_list": [b.book_id for b in br.books],
                "list_name": br.title,
                "list_content": br.description
            } for br in brs
        ]

        return {
            "status": 0,
            "msg": "获取成功",
            "data": data
        }


class CreateList(Resource):
    def post(self):
        """
        新建书单
        :return: 
        """
        args = get_request_params([
            ("uid", int, True, "json"),
            ("list_name", str, True, "json"),
            ("token", str, True, "json"),
            ("list_content", str, True, "json")
        ])

        uid = args["uid"]
        token = args["token"]
        list_name = args["list_name"]
        description = args["list_content"]

        user = User.verify_token(token)

        if (not user) or (user.id_ != uid):
            return {
                "status": 1,
                "msg": "未登录"
            }

        br = BookListModel(user_id=uid,
                           title=list_name,
                           description=description)

        try:
            db.session.add(br)
            db.session.commit()

            return {
                "status": 0,
                "msg": "创建成功"
            }

        except Exception as e:
            return {
                "status": 2,
                "msg": "服务器飞了"
            }


class ShowBookDetail(Resource):
    decorators = []

    def post(self):
        args = get_request_params([
            ("list_id", int, True, "json"),
            ("token", str, True, "json"),
            ("uid", int, True, "json")
        ])

        list_id = args["list_id"]

        bl = BookList.query.get(list_id)
        if not bl:
            return {"status": 1, "msg": "书单不存在"}

        books = bl.books
        return {
            "msg": "获取成功",
            "status": 0,
            "data": [
                {
                    "book_db_id": b.book_db_id,
                    "book_rate": b.book_rate,
                    "book_last_number": len(json.loads(b.detail_data)),
                    "book_id": b.book_id,
                    "book_cover": b.book_cover,
                    "book_author": json.loads(b.book_author),
                    "book_title": b.book_title,
                    "book_publish": b.book_publish
                } for b in books
            ]
        }


class RemoveBook(Resource):
    def post(self):
        args = get_request_params([
            ("book_id", int, True, "json"),
            ("list_id", int, True, "json"),
            ("token", str, True, "json"),
            ("uid", int, True, "json")
        ])

        user = User.verify_token(args["token"])

        if (not user) or (user.id_ != args["uid"]):
            return {
                "status": 1,
                "msg": "没有登录"
            }
        book_list = BookListModel.query.get(args["list_id"])
        if not book_list:
            return {
                "status": 2,
                "msg": "书单不存在"
            }

        if book_list.user_id != args["uid"]:
            return {
                "status": 3,
                "msg": "书单不是你的"
            }

        db.session.execute("delete from booklist_r WHERE book_id=:BID AND list_id=:LID",
                           params={"BID": args["book_id"], "LID": args["list_id"]})
        db.session.commit()

        return {
            "status": 0,
            "message": "删除成功"
        }


class FeedBack(Resource):
    decorators = []

    def post(self):
        args = get_request_params([
            ("token", int, True, "json"),
            ("contact", str, True, "json"),
            ("uid", int, True, "json"),
            ("timestamp", str, True, "json"),
            ("content", str, True, "json")
        ])

        token = args["token"]
        contact = args["contact"]
        uid = args["uid"]
        content = args["content"]

        user = User.verify_token(token)

        if (not user) or (user.id_ != uid):
            return {
                "status": 1,
                "msg": "未登录"
            }

        f = FeedBackModel(
            user_id=user.id_,
            contact=contact,
            date=datetime.now(),
            content=content
        )

        db.session.add(f)
        db.session.commit()

        return {"status": 0, "message": "反馈成功"}


class BorrowedBook(Resource):
    def post(self):
        args = get_request_params([
            ("token", str, True, "json"),
            ("uid", int, True, "json")
        ])
        user = User.verify_token(args["token"])
        if (not user) or (user.id_ != args["uid"]):
            return {
                "status": 1,
                "msg": "未登录"
            }

        b = Borrowed().get()
        return {
            "status": 0,
            "msg": "获取成功",
            "books": b
        }


class GetSubscribe(Resource):
    """获取订阅"""

    def post(self):
        args = get_request_params([
            ["token", str, True, "json"],
            ["uid", int, True, "json"]
        ])
        user = User.verify_token(args["token"])
        if (not user) or (user.id_ != args["uid"]):
            return {
                "status": 1,
                "msg": "未登录"
            }
        s = user.subscribing

        available = [i for i in s if i.book]
        books = [i.book for i in available]
        user.subscribing = available
        db.session.add(user)
        db.session.commit()

        return {
            "status": 0,
            "msg": "获取成功",
            "books": [{
                "book_last_number": book.book_last_number,
                "book_cover": book.book_cover,
                "book_id": book.book_id,
                "book_author": json.loads(book.book_author),
                "book_title": book.book_title,
                "book_db_id": book.book_db_id,
                "book_publish": book.book_publish,
                "book_rate": book.book_rate
            }
                for book in books]
        }


class Subscribe(Resource):
    """订阅"""

    def post(self):
        args = get_request_params([
            ["book_id", int, True, "json"],
            ["token", str, True, "json"],
            ["uid", int, True, "json"]
        ])
        user = User.verify_token(args["token"])
        if (not user) or (user.id_ != args["uid"]):
            return {
                "status": 1,
                "msg": "未登录"
            }
        result = db.session.execute("select * from subscribes WHERE user_id=:UID and book_id=:BID",
                                    params={"UID": args["uid"],
                                            "BID": args["book_id"]})
        result = result.fetchone()

        if result:
            return {
                "status": 1,
                "msg": "已经订阅了"
            }
        else:
            db.session.execute("insert into subscribes (user_id, book_id) VALUES (:UID, :BID)",
                               params={"UID": args["uid"],
                                       "BID": args["book_id"]})

        db.session.commit()
        return {
            "status": 0,
            "msg": "订阅成功"
        }


class RemoveSubscribe(Resource):
    """删除订阅"""

    def __init__(self):
        pass

    def post(self):
        args = get_request_params([
            ["book_id", int, True, "json"],
            ["token", str, True, "json"],
            ["uid", int, True, "json"]
        ])
        user = User.verify_token(args["token"])
        if (not user) or (user.id_ != args["uid"]):
            return {
                "status": 1,
                "msg": "未登录"
            }

        sub = SubModel.query.filter_by(user_id=args["uid"], book_id=args["book_id"]).first()

        db.session.delete(sub)
        db.session.commit()

        return {
            "status": 0,
            "msg": "删除成功"
        }


class RemoveList(Resource):
    """删除书单"""

    def post(self):
        args = get_request_params([
            ["list_id", int, True, "json"],
            ["token", str, True, "json"],
            ["uid", int, True, "json"]
        ])

        user = User.verify_token(args["token"])
        if (not user) or (user.id_ != args["uid"]):
            return {
                "status": 1,
                "msg": "未登录"
            }

        br = BookListModel.query.get(args["list_id"])

        if not br:
            return {"status": 1, "msg": "书单不存在"}

        if br.user_id != args["uid"]:
            return {"status": 2, "msg": "没有权限"}

        db.session.delete(br)
        db.session.commit()

        return {"status": 0, "msg": "删除成功"}


class SubscribeExist(Resource):
    """是否已经订阅"""

    def post(self):
        args = get_request_params([
            ["book_id", int, True, "json"],
            ["token", str, True, "json"],
            ["uid", int, True, "json"]
        ])
        user = User.verify_token(args["token"])
        if (not user) or (user.id_ != args["uid"]):
            return {
                "status": 1,
                "msg": "未登录"
            }
        sub = SubModel.query.filter_by(user_id=args["uid"], book_id=args["book_id"]).first()

        if sub:
            return {"status": 0, "msg": "获取成功", "is_subscribe": True}
        else:
            return {"status": 0, "msg": "获取成功", "is_subscribe": False}
