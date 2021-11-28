#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger
import hashlib


async def encryption(text, type):
    logger.info("[MD5] APP执行参数为: {text}", text=text)

    if type == "小写":
        my_hash = hashlib.md5()
        my_hash.update(str(text).encode("utf-8"))
        return {"status": 0, "result": str(my_hash.hexdigest())}
    else:
        my_hash = hashlib.md5()
        my_hash.update(str(text).encode("utf-8"))
        return {"status": 0, "result": str(my_hash.hexdigest()).upper()}
