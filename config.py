"""
Author: Tyan boot <tyanboot@outlook.com>
Date: 2017/6/18

"""


# -*- coding: utf-8 -*-

class Config(object):
    JOBS = [
        {
            "id": "book",
            "func": "yitu.services.gzhu.hotbook:task",
            "args": "",
            "trigger": {
                "type": "cron",
                "day": "*/1"
            }
        },
        {
            "id": "book_change",
            "func": "yitu.services.gzhu.change_book_detail:change_detail",
            "args": "",
            "trigger": {
                "type": "cron",
                "day": "*/1"
            }
        }
    ]

    SCHEDULER_API_ENABLED = True


class Product(Config):
    SQLALCHEMY_DATABASE_URI = """sqlite:///data.sqlite3"""
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    APP_KEY = "test-key"
    pass


class Develop(Config):
    SQLALCHEMY_DATABASE_URI = """mysql+pymysql://root:@localhost/yitu"""
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    pass


config = {
    "default": Develop,
    "dev": Develop
}
