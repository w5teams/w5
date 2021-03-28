#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger


async def hello_word(name):
    logger.info("[Hello Word] APP 执行参数为: {name}", name=name)
    return {"status": 0, "result": "Hello," + name}
