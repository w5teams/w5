#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger


async def execute(host, port, user, passwd, cmd):
    try:
        import winrm
    except:
        logger.info("[Win远程命令] 导入 winrm 模块失败, 请输入命令 pip install pywinrm")
        return {"status": 2, "result": "缺少 winrm 模块，请 pip install pywinrm 安装"}

    logger.info("[Win远程命令] APP执行参数为：{host} {port} {user} {passwd} {cmd}", host=host, port=port, user=user,
                passwd=passwd, cmd=cmd)

    try:
        win_server = winrm.Session('http://{host}:{port}/wsman'.format(host=host, port=port),
                                   auth=(user, passwd))
        r = win_server.run_cmd(cmd)
        return {"status": 0, "result": r.std_out.decode("utf-8")}
    except Exception as e:
        logger.info("[Win远程命令] 执行失败 ：{e}", e=e)
        return {"status": 2, "result": "执行失败"}
