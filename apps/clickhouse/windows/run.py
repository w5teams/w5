#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger


async def query(url, user, passwd, db, sql):
    try:
        from aiochclient import ChClient
        import aiohttp
        import traceback
    except:
        logger.info("[Clickhouse] 导入 aiochclient 模块失败, 请输入命令 pip install aiochclient")
        return {"status": 2, "result": "缺少 aoichclient 模块，请 pip install aiochclient 安装"}

    logger.info("[Clickhouse] APP执行参数为：{url} {database} {user} {passwd} {sql}", url=url, user=user, passwd=passwd,
                database=db, sql=sql)

    try:
        async with aiohttp.ClientSession() as s:
            client = ChClient(s, url=url, user=user, password=passwd, database=db)
            all_rows = await client.fetch(sql)
            result = []
            for row in all_rows:
                tmp = dict()
                for i in row.items():
                    tmp[i[0]] = i[1]
                result.append(tmp)
    except Exception as e:
        return {"status": 2, "result": str(e)}
    else:
        return {"status": 0, "result": result}
