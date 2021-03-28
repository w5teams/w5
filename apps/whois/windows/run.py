#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger
import requests


async def query(domain):
    logger.info("[Whois] APP执行参数为: {domain}", domain=domain)

    try:
        url = "https://api.devopsclub.cn/api/whoisquery?domain={domain}&type=json&standard=true".format(domain=domain)
        r = requests.get(url=url)
    except Exception as e:
        logger.error("[Whois] 请求 API 失败:{e}", e=e)
        return {"status": 2, "result": "请求 Whois API 失败"}

    if str(r.json()["data"]["status"]) == "1":
        return {"status": 1, "result": "域名解析失败"}
    elif str(r.json()["data"]["status"]) == "2":
        return {"status": 1, "result": "域名未注册"}
    elif str(r.json()["data"]["status"]) == "3":
        return {"status": 1, "result": "暂不支持此域名后缀查询"}
    elif str(r.json()["data"]["status"]) == "4":
        return {"status": 1, "result": "域名查询失败"}
    elif str(r.json()["data"]["status"]) == "5":
        return {"status": 1, "result": "请求数据错误"}

    return {"status": 0, "result": r.json()["data"]["data"]}
