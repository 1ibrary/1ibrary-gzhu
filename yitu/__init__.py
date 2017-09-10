"""
Author: Tyan boot <tyanboot@outlook.com>
Date: 2017/6/18

"""

# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from flask_apscheduler import APScheduler
from config import config

db = SQLAlchemy()
auth = HTTPTokenAuth("yitu-gzhu")
scheduler = APScheduler()


def create(cfg):
    yitu = Flask(__name__)
    yitu.config.from_object(config[cfg])
    db.init_app(yitu)
    db.app = yitu
    scheduler.init_app(yitu)
    scheduler.start()

    from yitu.resources import books_blue, users_blue
    yitu.register_blueprint(books_blue, url_prefix="/books")
    yitu.register_blueprint(users_blue, url_prefix="/users")

    return yitu
