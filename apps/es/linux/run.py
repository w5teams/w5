#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger


async def scan(host, port, index, body, account, password):
    try:
        from elasticsearch import Elasticsearch
    except:
        logger.info("[ES] 导入 Elasticsearch 模块失败, 请输入命令 pip install elasticsearch")
        return {"status": 2, "result": "缺少 Elasticsearch 模块，请 pip install elasticsearch 安装"}

    logger.info("[ES] APP执行参数为：{host} {port} {index} {body}", host=host, port=port, index=index, body=body)

    try:
        if account != None and str(account) != "" and password != None and str(password) != "":
            es = Elasticsearch(hosts=host, port=port, http_auth=(account, password))
        else:
            es = Elasticsearch(hosts=host, port=port)

        result = es.search(index=index, body=body)
    except Exception as e:
        return {"status": 2, "result": "ES连接失败:" + str(e)}
    return {"status": 0, "result": result}
