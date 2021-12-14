#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger


async def execute(host, port, user, passwd, shell):
    try:
        import socket
        import paramiko
    except:
        logger.info("[Linux远程命令] 导入 paramiko 模块失败, 请输入命令 pip install paramiko")
        return {"status": 2, "result": "缺少 paramiko 模块，请 pip install paramiko 安装"}

    logger.info("[Linux远程命令] APP执行参数为：{host} {port} {user} {passwd} {shell}", host=host, port=port, user=user,
                passwd=passwd, shell=shell)

    try:
        ssh = paramiko.SSHClient()
        key = paramiko.AutoAddPolicy()
        ssh.set_missing_host_key_policy(key)
        ssh.connect(host, int(port), user, passwd, timeout=5)
        stdin, stdout, stderr = ssh.exec_command(shell)
    except paramiko.ssh_exception.AuthenticationException:
        return {"status": 1, "result": "认证失败"}
    except paramiko.ssh_exception.NoValidConnectionsError:
        return {"status": 1, "result": "连接失败"}
    except socket.gaierror:
        return {"status": 1, "result": "Host 不正确"}
    except Exception as e:
        logger.info("[Linux远程命令] 执行失败 ：{e}", e=e)
        return {"status": 2, "result": "执行失败"}
    else:
        err = stderr.read()
        if err == b"":
            return {"status": 0, "result": str(stdout.read().decode("utf-8"))}
        else:
            return {"status": 2, "result": str(err.decode("utf-8"))}
