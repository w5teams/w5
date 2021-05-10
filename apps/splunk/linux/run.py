#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
import json
import base64
import asyncio
import requests
from loguru import logger


async def scan(domain, user, passwd, body):
    logger.info("[Splunk] APP执行参数为：{domain} {user} {passwd} {body}", domain=domain, user=user, passwd=passwd, body=body)

    try:
        # 设定http认证头
        headers = dict(Authorization='Basic ' + base64.b64encode(f'{user}:{passwd}'.encode('utf-8')).decode('utf-8'))
        body = dict(search='search ' + body)

        # 给splunk提交查询任务
        resp = requests.post(f'{domain}/services/search/jobs?output_mode=json', data=body, headers=headers)
        sid = resp.json().get('sid')
        logger.info("[Splunk] 任务已提交 sid: {sid}", sid=sid)

        # 获取任务状态，完成进行后续
        while True:
            try:
                resp = requests.get(f'{domain}/services/search/jobs/{sid}?output_mode=json', headers=headers)
                logger.info("[Splunk] 任务状态查询 状态: {status}",
                            status=resp.json().get('entry')[0].get('content').get('isDone'))
                if resp.json().get('entry')[0].get('content').get('isDone'):
                    break
                await asyncio.sleep(0.5)
            except Exception as e:
                logger.exception(e)

        # 获取查询任务结果
        resp = requests.get(f'{domain}/services/search/jobs/{sid}/results/', headers=headers, data='output_mode=json')
        result = resp.json()
    except Exception as e:
        return {"status": 2, "result": "Splunk查询失败:" + str(e)}

    return {"status": 0, "result": result}
