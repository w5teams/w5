#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger
import requests

threat_book_api = "https://api.threatbook.cn/v3"


async def ip_query(key, ip):
    logger.info("[微步威胁情报] APP执行参数为: {key} {ip}", key=key, ip=ip)

    try:
        url = threat_book_api + "/ip/query?lang=zh&apikey={key}&resource={ip}".format(key=key, ip=ip)
        r = requests.get(url=url)
    except Exception as e:
        logger.error("[微步威胁情报] 请求 API 失败:{e}", e=e)
        return {"status": 2, "result": "请求 微步威胁情报 API 失败"}

    return {"status": 0, "result": r.json()}


async def ip_reputation(key, ip):
    logger.info("[微步威胁情报] APP执行参数为: {key} {ip}", key=key, ip=ip)

    try:
        url = threat_book_api + "/scene/ip_reputation?lang=zh&apikey={key}&resource={ip}".format(key=key, ip=ip)
        r = requests.get(url=url)
    except Exception as e:
        logger.error("[微步威胁情报] 请求 API 失败:{e}", e=e)
        return {"status": 2, "result": "请求 微步威胁情报 API 失败"}

    return {"status": 0, "result": r.json()}


async def domain_query(key, domain):
    logger.info("[微步威胁情报] APP执行参数为: {key} {domain}", key=key, domain=domain)

    try:
        url = threat_book_api + "/domain/query?lang=zh&apikey={key}&resource={domain}".format(key=key, domain=domain)
        r = requests.get(url=url)
    except Exception as e:
        logger.error("[微步威胁情报] 请求 API 失败:{e}", e=e)
        return {"status": 2, "result": "请求 微步威胁情报 API 失败"}

    return {"status": 0, "result": r.json()}
