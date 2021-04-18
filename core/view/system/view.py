#!/usr/bin/env python
# encoding:utf-8
from . import *


@r.route("/get/system/list", methods=['GET', 'POST'])
def get_system_list():
    if request.method == "POST":
        setting = Setting.select('id', 'key', 'value').get()

        data = {}

        for s in setting:
            data[s.key] = s.value

        return Response.re(data=data)


@r.route("/post/system/w5key", methods=['GET', 'POST'])
def post_system_w5key():
    if request.method == "POST":
        w5key = request.json.get("w5key", "")

        Setting.where("key", "w5_key").update(
            {
                "value": w5key,
                "update_time": Time.get_date_time()
            }
        )

        redis.set("w5_key", str(w5key))
        return Response.re()


@r.route("/post/system/apikey", methods=['GET', 'POST'])
def post_system_apikey():
    if request.method == "POST":
        make_api_key()
        return Response.re()


@r.route("/post/system/del", methods=['GET', 'POST'])
def post_system_del():
    if request.method == "POST":
        type = request.json.get("type", 0)

        if type == 1:
            Workflow.where("id", "!=", "0").delete()
        elif type == 2:
            Logs.where("id", "!=", "0").delete()
        elif type == 3:
            Variablen.where("id", "!=", "0").delete()
        elif type == 4:
            redis.flushdb()
        elif type == 5:
            Report.where("id", "!=", "0").delete()

        return Response.re()


def get_w5_json():
    try:
        result = requests.get(url=current_app.config["update_path"] + "/w5.json", timeout=5)
        return result.json()["w5"]
    except Exception as e:
        return "fail"


def check_update():
    version_info = Version.select('name', 'version').get()

    w5_data = get_w5_json()

    data = {}

    if w5_data == "fail":
        data["is_w5"] = True
        data["w5"] = w5_data
        return data

    if VersionUtil.compare(str(w5_data["version"]), version_info[0].version) == ">":
        data["is_w5"] = True
        data["w5"] = w5_data
    else:
        data["is_w5"] = False

    return data


def update_version(w5_version):
    with db.transaction():
        Version.where('name', "w5").update(
            {
                "version": w5_version,
                "update_time": Time.get_date_time()
            }
        )


@r.route("/get/system/version", methods=['GET', 'POST'])
def post_system_version():
    if request.method == "POST":
        data = check_update()
        return Response.re(data=data)


@r.route("/get/system/w5json", methods=['GET', 'POST'])
def post_system_w5json():
    if request.method == "POST":
        w5_data = get_w5_json()
        return Response.re(data=w5_data)


def make_api_key():
    api_key = Random.make_token(string="api_key")

    Setting.where("key", "api_key").update(
        {
            "value": api_key,
            "update_time": Time.get_date_time()
        }
    )

    redis.set("api_key", str(api_key))


def init_key():
    setting = Setting.select("value").where('key', "api_key").first()

    if setting:
        if str(setting.value).strip() == "" or setting.value is None:
            make_api_key()


def init_timer():
    def setting():
        result = redis.set("manage_timer_lock", 1, nx=True, ex=30)
        if result:
            manage_timer = ManageTimer()
            manage_timer.start()

            s = ThreadedServer(service=manage_timer, port=53124, auto_register=False)
            s.start()

    t = threading.Thread(target=setting)
    t.setDaemon(True)
    t.start()
