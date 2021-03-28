#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger
import requests
import json


async def send(hook_uuid, msg):
    logger.info("[飞书通知] APP执行参数为: {hook_uuid} {text}", hook_uuid=hook_uuid, text=msg)

    headers = {'Content-Type': 'application/json;charset=UTF-8'}

    try:
        r = requests.post(
            url="https://open.feishu.cn/open-apis/bot/v2/hook/{hook_uuid}".format(hook_uuid=hook_uuid),
            data=json.dumps({
                "msg_type": "text",
                "content": {
                    "text": msg
                }
            }),
            headers=headers
        )
    except Exception as e:
        logger.error("[飞书通知] 请求飞书 API 失败:{e}", e=e)
        return {"status": 2, "result": "请求飞书 API 失败"}

    return {"status": 0, "result": r.json()}
