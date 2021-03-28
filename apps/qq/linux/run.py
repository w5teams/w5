#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger
import requests


async def query(qq):
    logger.info("[QQ] APP执行参数为: {qq}", qq=qq)

    try:
        url = "https://api.devopsclub.cn/api/qqinfo?qq={qq}".format(qq=qq)
        r = requests.get(url=url)
    except Exception as e:
        logger.error("[QQ] 请求 API 失败:{e}", e=e)
        return {"status": 2, "result": "请求 QQ API 失败"}

    if str(r.json()["code"]) == "0":
        return {"status": 0, "result": r.json()["data"]}

    else:
        return {"status": 1, "result": "查询不到 QQ 信息"}
