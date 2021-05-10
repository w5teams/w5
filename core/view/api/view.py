#!/usr/bin/env python
# encoding:utf-8
from . import *


@r.route("/webhook", methods=['GET', 'POST'])
def api_webhook():
    if request.method == "POST":
        api_key = request.json.get("key", "")
        app_uuid = request.json.get("uuid", "")
        text = request.json.get("text", "")

        if str(api_key).strip() == "" or api_key is None:
            return Response.re(err=ErrWebhookkey)

        if str(app_uuid).strip() == "" or app_uuid is None:
            return Response.re(err=ErrWebhookUUID)

        if str(text).strip() == "" or text is None:
            return Response.re(err=ErrWebhookText)

        key = "api_key"

        if redis.exists(key) == 0:
            setting = Setting.select('value').where("key", "api_key").first()
            value_key = setting.value
            redis.set("api_key", str(value_key))
        else:
            value_key = redis.get(key).decode()

        if str(api_key) != str(value_key):
            return Response.re(err=ErrWebhookKeyNot)

        workflow = Workflow.select('uuid', 'status', "controller_data").where("webhook_app", app_uuid).first()

        if workflow:
            if str(workflow.status) == "1":
                return Response.re(err=ErrWebhookStatus)
            else:
                print(00000)
                auto_execute(workflow.uuid, controller_data=workflow.controller_data, text=text, app_uuid=app_uuid)
                print(2222)

        else:
            return Response.re(err=ErrWebhookUUIDNot)

        return Response.re()


@r.route("/get/workflow_exec", methods=['GET', 'POST'])
def api_get_workflow_exec():
    if request.method == "POST":
        api_key = request.json.get("key", "")
        uuid = request.json.get("uuid", "")

        if str(api_key).strip() == "" or api_key is None:
            return Response.re(err=ErrWebhookkey)

        if str(uuid).strip() == "" or uuid is None:
            return Response.re(err=ErrWebhookUUID)

        key = "api_key"

        if redis.exists(key) == 0:
            setting = Setting.select('value').where("key", "api_key").first()
            value_key = setting.value
            redis.set("api_key", str(value_key))
        else:
            value_key = redis.get(key).decode()

        if str(api_key) != str(value_key):
            return Response.re(err=ErrWebhookKeyNot)

        from core.view.workflow.view import get_workflow_exec
        result = get_workflow_exec(uuid)
        return Response.re(data=result)


@r.route("/get/workflow_success_fail", methods=['GET', 'POST'])
def api_get_workflow_sucess_fail():
    if request.method == "POST":
        api_key = request.json.get("key", "")
        uuid = request.json.get("uuid", "")

        if str(api_key).strip() == "" or api_key is None:
            return Response.re(err=ErrWebhookkey)

        if str(uuid).strip() == "" or uuid is None:
            return Response.re(err=ErrWebhookUUID)

        key = "api_key"

        if redis.exists(key) == 0:
            setting = Setting.select('value').where("key", "api_key").first()
            value_key = setting.value
            redis.set("api_key", str(value_key))
        else:
            value_key = redis.get(key).decode()

        if str(api_key) != str(value_key):
            return Response.re(err=ErrWebhookKeyNot)

        from core.view.workflow.view import get_workflow_success_fail
        sum, success_sum, fail_sum = get_workflow_success_fail(uuid)

        data = {
            "success_sum": success_sum,
            "fail_sum": fail_sum
        }

        return Response.re(data=data)


@r.route("/get/workflow_logs", methods=['GET', 'POST'])
def api_get_workflow_logs():
    if request.method == "POST":
        api_key = request.json.get("key", "")
        uuid = request.json.get("uuid", "")

        if str(api_key).strip() == "" or api_key is None:
            return Response.re(err=ErrWebhookkey)

        if str(uuid).strip() == "" or uuid is None:
            return Response.re(err=ErrWebhookUUID)

        key = "api_key"

        if redis.exists(key) == 0:
            setting = Setting.select('value').where("key", "api_key").first()
            value_key = setting.value
            redis.set("api_key", str(value_key))
        else:
            value_key = redis.get(key).decode()

        if str(api_key) != str(value_key):
            return Response.re(err=ErrWebhookKeyNot)

        from core.view.workflow.view import get_workflow_logs
        logs_list = get_workflow_logs(uuid)
        return Response.re(data=logs_list.serialize())


@r.route("/get/executing", methods=['GET', 'POST'])
def api_get_executing():
    if request.method == "POST":
        api_key = request.json.get("key", "")
        uuid = request.json.get("uuid", "")

        if str(api_key).strip() == "" or api_key is None:
            return Response.re(err=ErrWebhookkey)

        key = "api_key"

        if redis.exists(key) == 0:
            setting = Setting.select('value').where("key", "api_key").first()
            value_key = setting.value
            redis.set("api_key", str(value_key))
        else:
            value_key = redis.get(key).decode()

        if str(api_key) != str(value_key):
            return Response.re(err=ErrWebhookKeyNot)

        if str(uuid).strip() == "" or uuid is None:
            if redis.exists("exec_sum") == 1:
                exec_sum = redis.get("exec_sum")
            else:
                exec_sum = 0
        else:
            if redis.exists(uuid + "&&exec_sum") == 1:
                exec_sum = redis.get(uuid + "&&exec_sum")
            else:
                exec_sum = 0

        return Response.re(data={"sum": exec_sum})
