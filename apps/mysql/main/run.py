#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger


async def query(host, port, user, passwd, db, sql):
    try:
        import pymysql
        import traceback
    except:
        logger.info("[Mysql] 导入 pymysql 模块失败, 请输入命令 pip install PyMySQL")
        return {"status": 2, "result": "缺少 pymysql 模块，请 pip install PyMySQL 安装"}

    logger.info("[Mysql] APP执行参数为：{host} {port} {user} {passwd} {db} {sql}", host=host, port=port, user=user,
                passwd=passwd, db=db, sql=sql)

    try:
        db = pymysql.connect(host=host, user=user, password=passwd, database=db, port=int(port))
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        return {"status": 2, "result": str(e)}
    else:
        db.close()
        return {"status": 0, "result": result}


async def update(host, port, user, passwd, db, sql):
    try:
        import pymysql
        import traceback
    except:
        logger.info("[Mysql] 导入 pymysql 模块失败, 请输入命令 pip install PyMySQL")
        return {"status": 2, "result": "缺少 pymysql 模块，请 pip install PyMySQL 安装"}

    logger.info("[Mysql] APP执行参数为：{host} {port} {user} {passwd} {db} {sql}", host=host, port=port, user=user,
                passwd=passwd, db=db, sql=sql)

    try:
        db = pymysql.connect(host=host, user=user, password=passwd, database=db, port=int(port))
        cursor = db.cursor()
        cursor.execute(sql)
    except Exception as e:
        try:
            db.rollback()
        except:
            pass
        return {"status": 2, "result": str(e)}
    else:
        db.commit()
        db.close()
        return {"status": 0, "result": "操作成功"}
