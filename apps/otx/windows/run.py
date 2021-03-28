#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger


async def is_ioc(api_key, pulse_id, ioc):
    try:
        from OTXv2 import OTXv2
    except:
        logger.info("[OTX] 导入 OTXv2 模块失败, 请输入命令 pip install OTXv2")
        return {"status": 2, "result": "缺少 OTXv2 模块，请 pip install OTXv2 安装"}

    logger.info("[OTX] APP执行参数为: {api_key} {pulse_id} {ioc}", api_key=api_key, pulse_id=pulse_id, ioc=ioc)

    otx = OTXv2(api_key)
    indicators = otx.get_pulse_indicators(pulse_id)
    iocs = []

    for indicator in indicators:
        iocs.append(indicator['indicator'])

    if ioc in iocs:
        return {"status": 0, "result": "True"}
    else:
        return {"status": 0, "result": "False"}
