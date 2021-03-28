#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger
import requests


async def ip(ip):
    logger.info("[IP 查询] APP执行参数为: {ip}", ip=ip)

    try:
        url = "http://ip-api.com/json/{ip}?lang=zh-CN".format(ip=ip)
        r = requests.get(url=url)
    except Exception as e:
        logger.error("[IP 查询] 请求 API 失败:{e}", e=e)
        return {"status": 2, "result": "请求 IP 查询 API 失败"}

    if r.json()["status"] == "success":
        result = r.json()["country"] + "," + r.json()["regionName"] + "," + r.json()["city"] + "," + \
                 str(r.json()["lat"]) + "," + str(r.json()["lon"])
        return {"status": 0, "result": result}
    else:
        return {"status": 2, "result": r.json()["status"]}
