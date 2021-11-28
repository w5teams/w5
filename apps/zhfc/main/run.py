#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger
import requests


async def make(text):
    logger.info("[中文分词] APP执行参数为: {text}", text=text)

    try:
        url = "https://api.devopsclub.cn/api/segcut?text={text}".format(text=text)
        r = requests.get(url=url)
    except Exception as e:
        logger.error("[中文分词] 请求 API 失败:{e}", e=e)
        return {"status": 2, "result": "请求 中文分词 API 失败"}

    if str(r.json()["code"]) == "0":
        return {"status": 0, "result": r.json()["data"]}
    else:
        return {"status": 1, "result": "分词失败"}
