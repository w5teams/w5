#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger
import requests
import json


async def send(access_token, msg):
    logger.info("[钉钉通知] APP执行参数为: {access_token} {text}", access_token=access_token, text=msg)

    headers = {'Content-Type': 'application/json;charset=UTF-8'}

    try:
        r = requests.post(
            url="https://oapi.dingtalk.com/robot/send?access_token={access_token}".format(access_token=access_token),
            data=json.dumps({
                "msgtype": "text",
                "text": {
                    "content": msg
                }
            }),
            headers=headers,
        )
    except Exception as e:
        logger.error("[钉钉通知] 请求钉钉 API 失败:{e}", e=e)
        return {"status": 2, "result": "请求钉钉 API 失败"}

    return {"status": 0, "result": r.json()}
