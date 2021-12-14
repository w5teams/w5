#!/usr/bin/env python
# encoding:utf-8
from . import *


@r.route("/get/user/list", methods=['GET', 'POST'])
def get_user_list():
    if request.method == "POST":
        keywords = request.json.get("keywords", "")
        page = request.json.get("page", 1)
        page_count = request.json.get("page_count", 10)

        if str(keywords) == "":
            user_list = Users.select(
                'id',
                'account',
                'nick_name',
                'email',
                'status',
                'update_time',
                'create_time',
                'avatar'
            ).order_by('id', 'desc').paginate(page_count, page)
        else:
            user_list = Users.select(
                'id',
                'account',
                'nick_name',
                'email',
                'update_time',
                'create_time',
                'avatar'
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
            ).order_by('id', 'desc').paginate(page_count, page)

        return Response.re(data=Page(model=user_list).to())


@r.route("/get/user/info", methods=['GET', 'POST'])
def get_user_info():
    if request.method == "POST":
        id = request.json.get("id", "")

        user_info = Users.select(
            'id',
            'account',
            'nick_name',
            'email',
            'update_time',
            'create_time',
            'avatar'
        ).where("id", id).first()

        return Response.re(data=user_info.serialize())


@r.route("/post/user/add", methods=['GET', 'POST'])
def post_user_add():
    if request.method == "POST":
        account = request.json.get("account", "")
        passwd = request.json.get("passwd", "")
        nick_name = request.json.get("nick_name", "")
        email = request.json.get("email", "")
        avatar = request.json.get("avatar", "")

        is_user_use = Users.where('account', account).first()

        if is_user_use:
            return Response.re(err=ErrUser)

        md5_password = Random.make_md5_password(string=passwd)

        Users.insert({
            'account': account,
            'passwd': md5_password,
            'nick_name': nick_name,
            'email': email,
            "avatar": avatar,
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
        avatar = request.json.get("avatar", "")

        if str(passwd) == "":
            Users.where('id', id).update(
                {
                    "nick_name": nick_name,
                    "email": email,
                    "avatar": avatar,
                    "update_time": Time.get_date_time()
                }
            )
        else:
            md5_password = Random.make_md5_password(string=passwd)

            Users.where('id', id).update(
                {
                    "nick_name": nick_name,
                    "email": email,
                    "avatar": avatar,
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


@r.route("/post/user/login_history", methods=['GET', 'POST'])
def post_user_login_history():
    if request.method == "POST":
        user_id = request.json.get("user_id", "")

        LoginHistory.insert({
            'user_id': user_id,
            'login_time': Time.get_date_time()
        })

        return Response.re()
