#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger



async def query_weather(city):
    # try:
    #     from urllib.parse import unquote,quote
    #     import requests
    # except:
    #     logger.info("[Query Weather] 导入 requests 模块失败，请输入命令 pip install requests")
    #     return 2,"缺少 requests模块"
    # url = "http://wthrcdn.etouch.cn/weather_mini?city="+quote(city,'utf-8')
    # r =await  str(requests.get(url=url).text.encode('utf-8').decode('utf-8'))

    return {"status": 0, "result": 'utf8'}
