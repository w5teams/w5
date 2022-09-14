#!/usr/bin/env python
# encoding:utf-8
import os
import requests
from core.utils.zip import Zip


class Cloud(object):
    def __init__(self, apps_path=None):
        self.api = "https://store.w5soar.com"
        self.apps_path = apps_path

    def upload(self, wid, name, type, author, email, description, version, github, app_dir):
        app_dir_path = "{apps_path}/{app_dir}".format(apps_path=self.apps_path, app_dir=app_dir)
        app_icon = "{app_dir}/icon.png".format(app_dir=app_dir_path)
        app_readme1 = "{app_dir}/readme.md".format(app_dir=app_dir_path)
        app_readme2 = "{app_dir}/README.md".format(app_dir=app_dir_path)
        save_name = "{app_dir}.zip".format(app_dir=app_dir_path)

        try:
            Zip.compress(app_dir_path, save_name)

            files = [
                ('files', open(app_icon, 'rb')),
                ('files', open(save_name, 'rb'))
            ]

            res = requests.post(self.api + "/api/v1/upload/app", files=files, verify=False)

            if res.json()["code"] != 0:
                return res.json()["msg"]

            zip_url = res.json()["zipUrl"]
            icon_url = res.json()["iconUrl"]
            doc = ""

            if os.path.exists(app_readme1):
                with open(app_readme1, "r") as f:
                    doc = f.read()

            if os.path.exists(app_readme2):
                with open(app_readme2, "r") as f:
                    doc = f.read()

            res = requests.post(self.api + "/api/v1/put/app", json={
                "wid": wid,
                "name": name,
                "icon": icon_url,
                "type": type,
                "author": author,
                "email": email,
                "description": description,
                "version": version,
                "doc": doc,
                "github": github,
                "downUrl": zip_url,
                "appDir": app_dir
            }, verify=False)

            return res.json()["msg"]
        except Exception as e:
            print(e)
            return "未知错误"
        finally:
            if os.path.exists(save_name):
                os.remove(save_name)

    def download(self, zip_url, app_dir, wid):
        file_name = app_dir + "_" + wid + ".zip"
        save_name = "{apps_path}/{file_name}".format(apps_path=self.apps_path, file_name=file_name)

        try:
            response = requests.get(zip_url)

            with open(save_name, "wb") as f:
                f.write(response.content)

            app_path = save_name.replace(".zip", "")

            bools, text = Zip.save(zip_path=save_name, save_path=app_path)

            return bools, text
        except Exception as e:
            print(e)
            return False, "网络异常"
        finally:
            if os.path.exists(save_name):
                os.remove(save_name)

    def list(self):
        url = self.api + "/api/v1/get/app"
        r = requests.get(url, verify=False)
        return r.json()["data"]

    def wid_info(self, wid):
        r = requests.get(self.api + "/api/v1/get/wid_info?wid=" + wid, verify=False)
        return r.json()["data"]
