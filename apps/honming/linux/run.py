#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger
import requests


async def query(domain):
    logger.info("[红名检测] APP执行参数为: {domain}", domain=domain)

    try:
        url = "https://api.devopsclub.cn/api/dcheck?url={domain}".format(domain=domain)
        r = requests.get(url=url)
    except Exception as e:
        logger.error("[红名检测] 请求 API 失败:{e}", e=e)
        return {"status": 2, "result": "请求 红名检测 API 失败"}

    if str(r.json()["code"]) == "0":
        return {"status": 0, "result": r.json()["data"]}
    else:
        return {"status": 1, "result": "查询不到 红名信息"}
