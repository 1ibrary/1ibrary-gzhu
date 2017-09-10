"""
Author: Tyan boot <tyanboot@outlook.com>
Date: 2017/6/20

"""

# -*- coding: utf-8 -*-

from yitu import auth
from yitu.models.user import User
from flask import g


@auth.verify_token
def verify_token(token):
    if not token:
        return False
    user = User.verify_token(token)

    if not user:
        return user
    g.user = user
    return True
