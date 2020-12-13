#!/usr/bin/env python
# encoding:utf-8
import os

no_path = ["__pycache__", "basic"]


class File():
    @staticmethod
    def find_apps(path):
        dir_list = []
        dir = os.listdir(path)

        dirs = [i for i in dir if os.path.isdir(os.path.join(path, i))]
        if dirs:
            for i in dirs:
                if i not in no_path:
                    dir_list.append(i)

        return dir_list

    @staticmethod
    def find_app_json(path, app_dir):
        app_json = path + "/" + app_dir + "/app.json"
        with open(app_json, 'rb') as f:
            return f.read()
