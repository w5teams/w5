#!/usr/bin/env python
# encoding:utf-8

import time


class Time(object):
    @staticmethod
    def get_date_time():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    @staticmethod
    def get_date():
        return time.strftime("%Y-%m-%d", time.localtime(time.time()))

    @staticmethod
    def get_timestamp():
        return str(int(round(time.time() * 1000)))
