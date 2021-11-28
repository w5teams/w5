#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger
import smtplib
from email.mime.text import MIMEText
from email.header import Header


async def send(host, port, user, passwd, encrypt, sender, to, title, type, text):
    logger.info("[E-Mail] APP执行参数为: {host} {port} {user} {passwd} {encrypt} {sender} {to} {title} {type} {text}", host=host,
                port=port, user=user, passwd=passwd, sender=sender, to=to,
                title=title, type=type, text=text, encrypt=encrypt)

    if type == "html":
        message = MIMEText(text, 'html', 'utf-8')
    else:
        message = MIMEText(text, 'plain', 'utf-8')

    message['Subject'] = Header(title, 'utf-8')
    message['From'] = sender

    try:
        if encrypt == 'none':
            w5_smtp = smtplib.SMTP()
            w5_smtp.connect(host, int(port))
        elif encrypt == 'tsl':
            w5_smtp = smtplib.SMTP(host, int(port))
            w5_smtp.starttls()
        else:
            w5_smtp = smtplib.SMTP_SSL(host, int(port))
        w5_smtp.login(user, passwd)
        w5_smtp.sendmail(sender, str(to).split(","), message.as_string())
        return {"status": 0, "result": "发送成功"}
    except Exception as e:
        logger.error("[E-Mail] 发送失败:{e}", e=e)
        return {"status": 2, "result": "邮件发送失败"}
