#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger
import base64


async def encryption(text):
    logger.info("[Base64] APP执行参数为: {text}", text=text)
    text = text.encode("utf-8")
    result = base64.b64encode(text)
    return {"status": 0, "result": str(result, 'utf8')}


async def decrypt(text):
    logger.info("[Base64] APP执行参数为: {text}", text=text)
    result = base64.b64decode(text).decode("utf-8")
    return {"status": 0, "result": str(result)}
