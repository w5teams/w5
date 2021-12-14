#!/usr/bin/env python
# encoding:utf-8
from . import *


@r.route("/get/type/list", methods=['GET', 'POST'])
def get_type_list():
    if request.method == "POST":
        type = request.json.get("type", "0")
        keywords = request.json.get("keywords", "")

        type_list = Types.select('id', 'type', 'name', 'update_time', 'create_time')

        if str(type) != "0":
            type_list = type_list.where("type", type)

        if str(keywords) == "":
            type_list = type_list.order_by('id', 'desc').get()
        else:
            type_list = type_list.or_where('name', 'like', '%{keywords}%'.format(keywords=keywords)).order_by(
                'id', 'desc').get()

        return Response.re(data=type_list.serialize())


@r.route("/post/type/add", methods=['GET', 'POST'])
def post_type_add():
    if request.method == "POST":
        type = request.json.get("type", "")
        name = request.json.get("name", "")

        is_type_use = Types.where('type', type).where('name', name).first()

        if is_type_use:
            return Response.re(err=ErrType)

        Types.insert({
            'type': type,
            'name': name,
            'update_time': Time.get_date_time(),
            'create_time': Time.get_date_time()
        })

        return Response.re()


@r.route("/post/type/update", methods=['GET', 'POST'])
def post_type_update():
    if request.method == "POST":
        id = request.json.get("id", "")
        type = request.json.get("type", "")
        name = request.json.get("name", "")

        is_type_use = Types.where('type', type).where('name', name).first()

        if is_type_use:
            return Response.re(err=ErrType)

        Types.where('id', id).update(
            {
                "name": name,
                "type": type,
                "update_time": Time.get_date_time()
            }
        )

        return Response.re()


@r.route("/post/type/del", methods=['GET', 'POST'])
def post_type_del():
    if request.method == "POST":
        id = request.json.get("id", "")
        type = request.json.get("type", "")

        db_name = ""

        if str(type) == "1":
            db_name = Workflow.__table__
        elif str(type) == "2":
            db_name = Variablen.__table__

        is_type_use = db.table(db_name).where('type_id', id).first()

        if is_type_use:
            return Response.re(err=ErrTypeUse)

        Types.where('id', id).delete()
        return Response.re()
