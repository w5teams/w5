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
                auto_execute(workflow.uuid, controller_data=workflow.controller_data, text=text, app_uuid=app_uuid)
        else:
            return Response.re(err=ErrWebhookUUIDNot)

        return Response.re()
