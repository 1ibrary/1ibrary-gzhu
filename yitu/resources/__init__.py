# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_restful import Api

from yitu.resources.books.main import HotBook, SearchBook, ShowDetail, Subscribe_, HotSearch
from yitu.resources.users.main import Login, CollectBook, \
    ShowBookDetail, FeedBack, ShowList, CreateList, RemoveBook, \
    BorrowedBook, GetSubscribe, RemoveSubscribe, Subscribe, RemoveList, \
    SubscribeExist

books_blue = Blueprint("books", __name__)
books_api = Api(books_blue)
books_api.add_resource(HotBook, "/hot_books")
books_api.add_resource(SearchBook, "/search_book")
books_api.add_resource(ShowDetail, "/show_detail")
books_api.add_resource(Subscribe_, "/subscribe")
books_api.add_resource(HotSearch, "/hot_search")

users_blue = Blueprint("users", __name__)
users_api = Api(users_blue)
users_api.add_resource(Login, "/login")
users_api.add_resource(CreateList, "/create_list")
users_api.add_resource(CollectBook, "/collect_book")
users_api.add_resource(RemoveBook, "/remove_book")
users_api.add_resource(ShowList, "/show_list")
users_api.add_resource(ShowBookDetail, "/show_detail")
users_api.add_resource(BorrowedBook, "/borrowed")
users_api.add_resource(RemoveList, "/remove_list")

users_api.add_resource(FeedBack, "/feedback")

users_api.add_resource(GetSubscribe, "/get_subscribe")
users_api.add_resource(Subscribe, "/subscribe")
users_api.add_resource(RemoveSubscribe, "/remove_subscribe")
users_api.add_resource(SubscribeExist, "/subscribe_exist")
