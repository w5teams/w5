#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger


async def get(host, port, db, password, key):
    try:
        import redis
    except:
        logger.info("[Redis] 导入 redis 模块失败, 请输入命令 pip install redis")
        return {"status": 2, "result": "缺少 Redis 模块，请 pip install redis 安装"}

    logger.info("[Redis] APP执行参数为: {host} {port} {db} {password} {key}", host=host, port=port, db=db, password=password,
                key=key)

    try:
        if str(password).strip() == "":
            r = redis.Redis(host=host, port=int(port), db=int(db), decode_responses=True)
        else:
            r = redis.Redis(host=host, port=int(port), db=int(db), password=str(password), decode_responses=True)

    except Exception as e:
        logger.error("[Redis] 执行失败:{e}", e=e)
        return {"status": 2, "result": "Redis 执行失败"}

    return {"status": 0, "result": r.get(key)}


async def set(host, port, db, password, key, value):
    try:
        import redis
    except:
        logger.info("[Redis] 导入 redis 模块失败, 请输入命令 pip install redis")
        return {"status": 2, "result": "缺少 Redis 模块，请 pip install redis 安装"}

    logger.info("[Redis] APP执行参数为: {host} {port} {db} {password} {key} {value}", host=host, port=port, db=db,
                password=password,
                key=key, value=value)

    try:
        if str(password).strip() == "":
            r = redis.Redis(host=host, port=int(port), db=int(db), decode_responses=True)
        else:
            r = redis.Redis(host=host, port=int(port), db=int(db), password=str(password), decode_responses=True)

    except Exception as e:
        logger.error("[Redis] 执行失败:{e}", e=e)
        return {"status": 2, "result": "Redis 执行失败"}

    return {"status": 0, "result": r.set(key, value)}


async def delete(host, port, db, password, key):
    try:
        import redis
    except:
        logger.info("[Redis] 导入 redis 模块失败, 请输入命令 pip install redis")
        return {"status": 2, "result": "缺少 Redis 模块，请 pip install redis 安装"}

    logger.info("[Redis] APP执行参数为: {host} {port} {db} {password} {key}", host=host, port=port, db=db,
                password=password,
                key=key)

    try:
        if str(password).strip() == "":
            r = redis.Redis(host=host, port=int(port), db=int(db), decode_responses=True)
        else:
            r = redis.Redis(host=host, port=int(port), db=int(db), password=str(password), decode_responses=True)

    except Exception as e:
        logger.error("[Redis] 执行失败:{e}", e=e)
        return {"status": 2, "result": "Redis 执行失败"}

    return {"status": 0, "result": r.delete(key)}


async def flushdb(host, port, db, password):
    try:
        import redis
    except:
        logger.info("[Redis] 导入 redis 模块失败, 请输入命令 pip install redis")
        return {"status": 2, "result": "缺少 Redis 模块，请 pip install redis 安装"}

    logger.info("[Redis] APP执行参数为: {host} {port} {db} {password}", host=host, port=port, db=db,
                password=password)

    try:
        if str(password).strip() == "":
            r = redis.Redis(host=host, port=int(port), db=int(db), decode_responses=True)
        else:
            r = redis.Redis(host=host, port=int(port), db=int(db), password=str(password), decode_responses=True)

    except Exception as e:
        logger.error("[Redis] 执行失败:{e}", e=e)
        return {"status": 2, "result": "Redis 执行失败"}

    return {"status": 0, "result": r.flushdb()}


async def flushall(host, port, password):
    try:
        import redis
    except:
        logger.info("[Redis] 导入 redis 模块失败, 请输入命令 pip install redis")
        return {"status": 2, "result": "缺少 Redis 模块，请 pip install redis 安装"}

    logger.info("[Redis] APP执行参数为: {host} {port} {password}", host=host, port=port,
                password=password)

    try:
        if str(password).strip() == "":
            r = redis.Redis(host=host, port=int(port), decode_responses=True)
        else:
            r = redis.Redis(host=host, port=int(port), password=str(password), decode_responses=True)

    except Exception as e:
        logger.error("[Redis] 执行失败:{e}", e=e)
        return {"status": 2, "result": "Redis 执行失败"}

    return {"status": 0, "result": r.flushall()}
