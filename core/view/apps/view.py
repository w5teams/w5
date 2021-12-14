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

        del_path = current_app.config["apps_path"] + "/" + str(app_dir).replace(".", "").replace("/", "")

        try:
            shutil.rmtree(del_path)
        except Exception as e:
            return Response.re(err=ErrAppDel)
        else:
            return Response.re()


@r.route("/post/app/import", methods=['GET', 'POST'])
def post_app_import():
    if request.method == "POST":
        f = request.files['file']

        filename = secure_filename(f.filename)

        if filename.split('.')[-1] == "zip":
            tmp_dir = current_app.config["tmp_path"]
            app_dir = current_app.config["apps_path"]

            if os.path.exists(tmp_dir) == False:
                os.makedirs(tmp_dir)

            file_path = tmp_dir + "/" + filename
            f.save(file_path)

            save_path = app_dir + "/" + filename.replace(".zip", "")

            if os.path.exists(save_path):
                return Response.re(err=ErrUploadAppExist)

            status = Zip.save(zip_path=file_path, save_path=save_path)

            if status:
                shutil.rmtree(tmp_dir)
                return Response.re()
            else:
                shutil.rmtree(tmp_dir)
                return Response.re(err=ErrUploadZipR)
        else:
            return Response.re(err=ErrUploadZip)
