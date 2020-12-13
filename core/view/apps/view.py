#!/usr/bin/env python
# encoding:utf-8
from . import *


@r.route("/get/app/list", methods=['GET', 'POST'])
def get_app_list():
    if request.method == "GET":
        app_data = {}

        dir_list = File.find_apps(path=current_app.config["apps_path"])

        for d in dir_list:
            app_json = File.find_app_json(path=current_app.config["apps_path"], app_dir=d)

            app_d = json.loads(app_json)

            app_d["app_dir"] = d
            app_d["icon"] = d + "/icon.png"

            app_data[d] = app_d

        return Response.re(data=app_data)


@r.route("/post/app/del", methods=['GET', 'POST'])
def post_app_del():
    if request.method == "POST":
        app_dir = request.json.get("app_dir", "")
        del_path = current_app.config["apps_path"] + "/" + app_dir

        try:
            shutil.rmtree(del_path)
        except Exception as e:
            return Response.re(err=ErrAppDel)
        else:
            return Response.re()
