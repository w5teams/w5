#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger
import requests


async def send(key, text, desp):
    logger.info("[Server酱] APP执行参数为: {key} {text} {desp}", key=key, text=text, desp=desp)

    try:
        url = "https://sc.ftqq.com/{key}.send".format(key=key)

        if str(desp).strip() == "":
            data = {
                'text': text
            }
        else:
            data = {
                'text': text,
                'desp': desp
            }

        r = requests.post(url=url, data=data)
    except Exception as e:
        logger.error("[Server酱] 请求 API 失败:{e}", e=e)
        return {"status": 2, "result": "请求 Server酱 API 失败"}

    if r.json()["errno"] == 0:
        return {"status": 0, "result": r.json()}
    else:
        return {"status": 2, "result": r.json()}
