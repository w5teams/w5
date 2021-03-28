#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger
import requests


async def query(phone):
    logger.info("[手机号归属地] APP执行参数为: {phone}", phone=phone)

    try:
        url = "https://api.devopsclub.cn/api/telquery?tel={phone}".format(phone=phone)
        r = requests.get(url=url)
    except Exception as e:
        logger.error("[手机号归属地] 请求 API 失败:{e}", e=e)
        return {"status": 2, "result": "请求 手机号归属地 API 失败"}

    if str(r.json()["code"]) == "0":
        return {"status": 0, "result": r.json()["data"]}
    else:
        return {"status": 1, "result": "查询不到手机号归属地"}
