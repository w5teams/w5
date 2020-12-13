#!/usr/bin/env python
# encoding:utf-8
from . import *


@r.route("/get/user/list", methods=['GET', 'POST'])
def get_user_list():
    if request.method == "POST":
        keywords = request.json.get("keywords", "")

        if str(keywords) == "":
            user_list = Users.select(
                'id',
                'account',
                'nick_name',
                'email',
                'status',
                'update_time',
                'create_time'
            ).order_by('id', 'desc').get()
        else:
            user_list = Users.select(
                'id',
                'account',
                'nick_name',
                'email',
                'update_time',
                'create_time'
            ).where(
                'account',
                'like',
                '%{keywords}%'.format(keywords=keywords)
            ).or_where(
                'nick_name',
                'like',
                '%{keywords}%'.format(keywords=keywords)
            ).or_where(
                'email',
                'like',
                '%{keywords}%'.format(keywords=keywords)
            ).order_by('id', 'desc').get()

        return Response.re(data=user_list.serialize())


@r.route("/post/user/add", methods=['GET', 'POST'])
def post_user_add():
    if request.method == "POST":
        account = request.json.get("account", "")
        passwd = request.json.get("passwd", "")
        nick_name = request.json.get("nick_name", "")
        email = request.json.get("email", "")

        is_user_use = Users.where('account', account).first()

        if is_user_use:
            return Response.re(err=ErrUser)

        md5_password = Random.make_md5_password(string=passwd)

        Users.insert({
            'account': account,
            'passwd': md5_password,
            'nick_name': nick_name,
            'email': email,
            'status': 0,
            'update_time': Time.get_date_time(),
            'create_time': Time.get_date_time()
        })

        return Response.re()


@r.route("/post/user/update", methods=['GET', 'POST'])
def post_user_update():
    if request.method == "POST":
        id = request.json.get("id", "")
        nick_name = request.json.get("nick_name", "")
        email = request.json.get("email", "")
        passwd = request.json.get("passwd", "")

        if str(passwd) == "":
            Users.where('id', id).update(
                {
                    "nick_name": nick_name,
                    "email": email,
                    "update_time": Time.get_date_time()
                }
            )
        else:
            md5_password = Random.make_md5_password(string=passwd)

            Users.where('id', id).update(
                {
                    "nick_name": nick_name,
                    "email": email,
                    "passwd": md5_password,
                    "update_time": Time.get_date_time()
                }
            )

        return Response.re()


@r.route("/post/user/del", methods=['GET', 'POST'])
def post_user_del():
    if request.method == "POST":
        id = request.json.get("id", "")
        token = request.headers.get("token")

        is_user_use = Users.where('token', token).first()

        if str(is_user_use.id) == str(id):
            return Response.re(err=ErrUserDel)

        Users.where('id', id).delete()

        return Response.re()


@r.route("/post/user/status", methods=['GET', 'POST'])
def post_user_status():
    if request.method == "POST":
        id = request.json.get("id", "")
        status = request.json.get("status", "")
        token = request.headers.get("token")

        is_user_use = Users.where('token', token).first()

        if str(is_user_use.id) == str(id):
            return Response.re(err=ErrUserSwitch)

        Users.where('id', id).update(
            {
                "status": status,
                "update_time": Time.get_date_time()
            }
        )

        return Response.re()
