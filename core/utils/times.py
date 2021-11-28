#!/usr/bin/env python
# encoding:utf-8

import time
import datetime
import calendar
from datetime import timedelta


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

    @staticmethod
    def get_hour():
        result = []
        for i in range(24):
            if i >= 10:
                result.append(str(i))
            else:
                result.append("0" + str(i))

        return result

    @staticmethod
    def get_week():
        result = []
        now = datetime.datetime.now()
        for i in range(7):
            curr_week = now + timedelta(days=i - now.weekday())
            arr = str(curr_week).split(" ")[0].split("-")
            v = arr[1] + "-" + arr[2]
            result.append(v)

        return result

    @staticmethod
    def get_month():
        result = []
        now = datetime.datetime.now()

        curr_year_month = datetime.datetime(now.year, now.month, 1)
        index = calendar.monthrange(int(str(curr_year_month).split("-")[0]), int(str(curr_year_month).split("-")[1]))[1]

        for i in range(index)[::-1]:
            curr_month = datetime.datetime(now.year, now.month + 1, 1) - timedelta(days=i + 1)
            arr = str(curr_month).split(" ")[0].split("-")
            v = arr[1] + "-" + arr[2]
            result.append(v)

        return result

    @staticmethod
    def get_upper_month():
        result = []
        now = datetime.datetime.now()

        this_year_month = datetime.datetime(now.year, now.month, 1)
        curr_year_month = this_year_month - timedelta(days=1)
        index = calendar.monthrange(int(str(curr_year_month).split("-")[0]), int(str(curr_year_month).split("-")[1]))[1]

        for i in range(index)[::-1]:
            curr_month = this_year_month - timedelta(days=i + 1)
            arr = str(curr_month).split(" ")[0].split("-")
            v = arr[1] + "-" + arr[2]
            result.append(v)

        return result

    @staticmethod
    def get_year():
        result = []
        for i in range(12):
            if i + 1 >= 10:
                result.append(str(i + 1))
            else:
                result.append("0" + str(i + 1))

        return result
