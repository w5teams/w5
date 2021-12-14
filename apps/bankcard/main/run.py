#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger
import requests


async def query(card):
    logger.info("[银行卡查询] APP执行参数为: {card}", card=card)

    try:
        url = "https://api.devopsclub.cn/api/bankcard?bakCard={card}".format(card=card)
        r = requests.get(url=url)
    except Exception as e:
        logger.error("[银行卡查询] 请求 API 失败:{e}", e=e)
        return {"status": 2, "result": "请求 银行卡查询 API 失败"}

    if str(r.json()["code"]) == "0":
        return {"status": 0, "result": r.json()["data"]}
    else:
        return {"status": 1, "result": "查询不到银行卡信息"}
