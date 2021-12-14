#!/usr/bin/env python
# encoding:utf-8
import random
import time
import hashlib
import uuid


class Random(object):
    @staticmethod
    def make_code(length=4):
        code_list = []
        for i in range(10):
            code_list.append(str(i))
        my_slice = random.sample(code_list, length)
        number = ''
        for n in my_slice:
            number += n + ''
        return number

    @staticmethod
    def make_order_number(length=5):
        number = Random.make_code(length=length)
        times = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        return str(times) + '' + str(number)

    @staticmethod
    def make_md5(string=""):
        my_hash = hashlib.md5()
        my_hash.update(str(string).encode("utf-8"))
        return str(my_hash.hexdigest()).upper()

    @staticmethod
    def make_token(string=""):
        number = Random.make_code(length=10)
        times = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        result = Random.make_md5(string=string + "" + times + '' + number)
        return result

    @staticmethod
    def make_md5_password(string=""):
        result = Random.make_md5(string=string)
        md5_password = Random.make_md5(string=result + "&&w5.io")
        return md5_password

    @staticmethod
    def make_uuid():
        return uuid.uuid1()
