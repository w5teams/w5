#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger
import requests


async def make(url):
    logger.info("[短连接生成] APP执行参数为: {url}", url=url)

    return {"status": 2, "result": "生成失败"}
