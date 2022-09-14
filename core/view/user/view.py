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
            user_list = Users.join(
                UserRole.__table__,
                Users.__table__ + '.id',
                '=',
                UserRole.__table__ + '.user_id'
            ).join(
                Role.__table__,
                UserRole.__table__ + '.role_id',
                '=',
                Role.__table__ + '.id'
            ).select(
                Users.__table__ + '.id',
                Users.__table__ + '.account',
                Users.__table__ + '.nick_name',
                Users.__table__ + '.email',
                Users.__table__ + '.status',
                Users.__table__ + '.update_time',
                Users.__table__ + '.create_time',
                Users.__table__ + '.avatar',
                Role.__table__ + '.id as role_id',
                Role.__table__ + '.name as role_name',
            ).order_by('id', 'desc').paginate(page_count, page)
        else:
            user_list = Users.join(
                UserRole.__table__,
                Users.__table__ + '.id',
                '=',
                UserRole.__table__ + '.user_id'
            ).join(
                Role.__table__,
                UserRole.__table__ + '.role_id',
                '=',
                Role.__table__ + '.id'
            ).select(
                Users.__table__ + '.id',
                Users.__table__ + '.account',
                Users.__table__ + '.nick_name',
                Users.__table__ + '.email',
                Users.__table__ + '.status',
                Users.__table__ + '.update_time',
                Users.__table__ + '.create_time',
                Users.__table__ + '.avatar',
                Role.__table__ + '.id as role_id',
                Role.__table__ + '.name as role_name',
            ).where(
                Users.__table__ + '.account',
                'like',
                '%{keywords}%'.format(keywords=keywords)
            ).or_where(
                Users.__table__ + '.nick_name',
                'like',
                '%{keywords}%'.format(keywords=keywords)
            ).or_where(
                Users.__table__ + '.email',
                'like',
                '%{keywords}%'.format(keywords=keywords)
            ).order_by('id', 'desc').paginate(page_count, page)

        return Response.re(data=Page(model=user_list).to())


@r.route("/get/user/simple_list", methods=['GET', 'POST'])
def get_user_simple_list():
    if request.method == "POST":
        sql = '''
        select id,nick_name from `w5_users` where status=0 ORDER BY CONVERT(nick_name USING GBK);
        '''
        result = db.select(sql)
        return Response.re(data=result)


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
        role_id = request.json.get("role_id", "")

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

        user_info = Users.select('id').where('account', account).first()

        UserRole.where('user_id', user_info.id).delete()

        UserRole.insert({
            'user_id': user_info.id,
            'role_id': role_id,
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
        role_id = request.json.get("role_id", "")

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

        UserRole.where('user_id', id).delete()

        UserRole.insert({
            'user_id': id,
            'role_id': role_id,
            'create_time': Time.get_date_time()
        })

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


@r.route("/get/nav/list", methods=['GET', 'POST'])
def get_nav_list():
    if request.method == "POST":
        nav_list = Nav.select(
            'id',
            'name',
        ).order_by('order', 'asc').get()

        result = []

        for nav in nav_list:
            result.append({
                "key": str(nav.id),
                "name": nav.name
            })

        return Response.re(data=result)


@r.route("/get/role/list", methods=['GET', 'POST'])
def get_role_list():
    if request.method == "POST":
        role_list = Role.select(
            'id',
            'name',
            'remarks',
            'update_time'
        ).get()

        return Response.re(data=role_list.serialize())


@r.route("/get/role_nav/list", methods=['GET', 'POST'])
def get_role_nav_list():
    if request.method == "POST":
        role_id = request.json.get("role_id", "")

        role_nav_list = RoleNav.select(
            'nav_id'
        ).where('role_id', role_id).get()

        result = set([])

        for nav in role_nav_list:
            result.add(str(nav.nav_id))

        return Response.re(data=list(result))


@r.route("/get/user_nav/list", methods=['GET', 'POST'])
def get_user_nav_list():
    if request.method == "POST":
        user_id = request.json.get("user_id", "")

        nav_list = UserRole.join(
            Role.__table__,
            UserRole.__table__ + '.role_id',
            '=',
            Role.__table__ + '.id'
        ).join(
            RoleNav.__table__,
            Role.__table__ + '.id',
            '=',
            RoleNav.__table__ + '.role_id'
        ).join(
            Nav.__table__,
            Nav.__table__ + '.id',
            '=',
            RoleNav.__table__ + '.nav_id'
        ).distinct().select(
            Nav.__table__ + '.name',
            Nav.__table__ + '.path',
            Nav.__table__ + '.key',
            Nav.__table__ + '.icon',
            Nav.__table__ + '.is_menu',
            Nav.__table__ + '.order'
        ).where(
            UserRole.__table__ + '.user_id', user_id
        ).order_by('order', 'asc').get()

        result = []

        for nav in nav_list:
            result.append({
                "name": nav.name,
                "path": nav.path,
                "key": nav.key,
                "icon": nav.icon,
                "is_menu": nav.is_menu
            })

        return Response.re(data=result)


@r.route("/post/role_nav/add", methods=['GET', 'POST'])
def post_role_nav_add():
    if request.method == "POST":
        id = request.json.get("id", "")
        name = request.json.get("name", "")
        nav_key = request.json.get("nav_key", "")
        remarks = request.json.get("remarks", "")

        if id == 0:
            is_exist = Role.select('name').where('name', name).first()

            if is_exist:
                return Response.re(err=ErrRoleExist)

            Role.insert_get_id({
                'name': name,
                'remarks': remarks,
                'update_time': Time.get_date_time(),
                'create_time': Time.get_date_time()
            })

            role_info = Role.select('id').where('name', name).first()

            for nav in nav_key:
                RoleNav.insert({
                    'role_id': role_info.id,
                    'nav_id': nav,
                    'create_time': Time.get_date_time()
                })
        else:
            Role.where('id', id).update(
                {
                    "name": name,
                    "remarks": remarks,
                    "update_time": Time.get_date_time()
                }
            )

            RoleNav.where('role_id', id).delete()

            for nav in nav_key:
                RoleNav.insert({
                    'role_id': id,
                    'nav_id': nav,
                    'create_time': Time.get_date_time()
                })

        return Response.re()


@r.route("/post/role_nav/del", methods=['GET', 'POST'])
def post_role_nav_del():
    if request.method == "POST":
        id = request.json.get("id", "")

        Role.where('id', id).delete()
        RoleNav.where('role_id', id).delete()

        return Response.re()
