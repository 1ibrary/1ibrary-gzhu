"""
Author: Tyan boot <tyanboot@outlook.com>
Date: 2017/6/18

"""

# -*- coding: utf-8 -*-
from flask_restful import reqparse


def get_request_params(params):
    """
    parse args from request, and return a dict
    :param params: the params to parse
    :type params: list

    :return: dict

    eg:
    params = [
               ("name", str, True, ["headers", "cookies"]),
               ("password", str, True, ["args", "form"])
             ]
    """
    parser = reqparse.RequestParser()
    for p in params:
        parser.add_argument(p[0], type=p[1], required=p[2], location=p[3])

    return parser.parse_args()
