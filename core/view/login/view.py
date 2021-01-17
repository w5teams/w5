#!/usr/bin/env python
# encoding:utf-8
from . import *


@r.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        account = request.json.get("account", "")
        passwd = request.json.get("passwd", "")

        user = Users.where('account', account).or_where('email', account).first()

        if user is None:
            return Response.re(err=ErrUserNot)

        if user.status == 1:
            return Response.re(err=ErrUserLoginSwitch)

        md5_password = Random.make_md5_password(string=str(passwd))

        if md5_password == user.passwd:

            token = Random.make_token(string=account)

            redis.set(token, str(user.id), ex=60 * 60 * 24 * 7)

            Users.where('id', user.id).update(
                {
                    "token": token,
                    "update_time": Time.get_date_time()
                }
            )

            return Response.re(data={"token": token, "account": user.account, "nick_name": user.nick_name,
                                     "user_id": user.id})
        else:
            return Response.re(err=ErrUserPassword)
