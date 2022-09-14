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

            status, text = Zip.save(zip_path=file_path, save_path=save_path)

            if status:
                shutil.rmtree(tmp_dir)
                return Response.re()
            else:
                shutil.rmtree(tmp_dir)
                return Response.re(err=ErrMsg(errcode=9030, errmsg=text))
        else:
            return Response.re(err=ErrUploadZip)


@r.route("/post/app/upload", methods=['GET', 'POST'])
def post_app_upload():
    if request.method == "POST":
        wid = request.json.get("wid", "")
        name = request.json.get("name", "")
        type = request.json.get("type", "")
        author = request.json.get("author", "")
        email = request.json.get("email", "")
        description = request.json.get("description", "")
        version = request.json.get("version", "")
        github = request.json.get("github", "")
        app_dir = request.json.get("app_dir", "")

        result = Cloud(apps_path=current_app.config["apps_path"]).upload(
            wid,
            name,
            type,
            author,
            email,
            description,
            version,
            github,
            app_dir
        )

        if result == "success":
            return Response.re()
        else:
            return Response.re(err=ErrMsg(errcode=9028, errmsg=result))


@r.route("/post/app/download", methods=['GET', 'POST'])
def post_app_download():
    if request.method == "POST":
        zip_url = request.json.get("zip_url", "")
        app_dir = request.json.get("app_dir", "")
        wid = request.json.get("wid", "")

        bools, text = Cloud(apps_path=current_app.config["apps_path"]).download(
            zip_url=zip_url,
            app_dir=app_dir,
            wid=wid
        )

        if bools:
            return Response.re()
        else:
            return Response.re(err=ErrMsg(errcode=9029, errmsg=text))


@r.route("/get/app/cloud_list", methods=['GET', 'POST'])
def post_app_cloud_list():
    if request.method == "POST":
        result = Cloud().list()
        return Response.re(data=result)


@r.route("/get/app/cloud_info", methods=['GET', 'POST'])
def post_app_cloud_info():
    if request.method == "POST":
        wid = request.json.get("wid", "")
        print(wid)
        result = Cloud().wid_info(wid=wid)
        return Response.re(data=result)
