# -*- coding: utf-8 -*-
"""
 Created by TyanBoot on 2017/3/30
 Tyan <tyanboot@outlook.com>

"""

from os import remove

import requests
from PIL import Image
from bs4 import BeautifulSoup
from pytesseract import image_to_string


class Login(object):
    def __init__(self):
        self.index_url = 'http://210.35.251.243/reader/login.php'
        self.capture_url = 'http://210.35.251.243/reader/captcha.php'
        self.login_url = 'http://210.35.251.243/reader/redr_verify.php'
        self.data = None
        self.cookies = None

    def before_login(self):
        self.data = requests.get(self.index_url)
        self.data.encoding = 'utf-8'
        self.cookies = self.data.cookies

    def get_capture(self):
        data = requests.get(self.capture_url, cookies=self.cookies)
        with open("./img_cache/" + self.cookies['PHPSESSID'] + ".gif", "wb+") as f:
            f.write(data.content)

        gif = Image.open("./img_cache/" + self.cookies['PHPSESSID'] + ".gif")

        png = Image.new("RGB", gif.size)
        png.paste(gif)

        str = image_to_string(png).strip()
        remove("./img_cache/" + self.cookies['PHPSESSID'] + ".gif")

        return str

    def login(self, user, password):
        self.before_login()

        chk_code = self.get_capture()

        post_data = {
            'number': user,
            'passwd': password,
            'captcha': chk_code,
            'select': 'cert_no',
            'returnUrl': ''
        }

        data = requests.post(self.login_url, cookies=self.cookies, data=post_data)
        data.encoding = 'utf-8'

        soup = BeautifulSoup(data.text, "lxml")
        status = soup.select(".header_right_font")[1].find_all("a")[1].text

        if status == "注销":
            name = soup.select_one(".profile-name").text
            return self.cookies["PHPSESSID"], name
        else:
            return False, None
