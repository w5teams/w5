#!/usr/bin/env python
# encoding:utf-8
from . import *


@r.route("/get/variablen/list", methods=['GET', 'POST'])
def get_variablen_list():
    if request.method == "POST":
        type = request.json.get("type", "0")
        keywords = request.json.get("keywords", "")

        variablen_list = Variablen.join(
            Types.__table__,
            Variablen.__table__ + '.type_id',
            '=',
            Types.__table__ + '.id'
        ).select(
            Variablen.__table__ + '.id',
            Variablen.__table__ + '.type_id',
            Types.__table__ + '.name as type_name',
            Variablen.__table__ + '.key',
            Variablen.__table__ + '.value',
            Variablen.__table__ + '.remarks',
            Variablen.__table__ + '.status',
            Variablen.__table__ + '.update_time',
            Variablen.__table__ + '.create_time'
        )

        if str(type) != "0":
            variablen_list = variablen_list.where("type_id", type)

        if str(keywords) == "":
            variablen_list = variablen_list.order_by("id", 'desc').get()
        else:
            variablen_list = variablen_list.or_where(
                'key',
                'like',
                '%{keywords}%'.format(keywords=keywords)
            ).or_where(
                'value',
                'like',
                '%{keywords}%'.format(keywords=keywords)
            ).order_by('id', 'desc').get()

        return Response.re(data=variablen_list.serialize())


@r.route("/post/variablen/add", methods=['GET', 'POST'])
def post_variablen_add():
    if request.method == "POST":
        type_id = request.json.get("type_id", "")
        key = request.json.get("key", "")
        value = request.json.get("value", "")
        remarks = request.json.get("remarks", "")

        is_key_use = Variablen.where('key', key).first()

        if is_key_use:
            return Response.re(err=ErrVariablenUse)

        Variablen.insert({
            'type_id': type_id,
            'key': key,
            'value': value,
            'remarks': remarks,
            'status': 0,
            'update_time': Time.get_date_time(),
            'create_time': Time.get_date_time()
        })

        return Response.re()


@r.route("/post/variablen/update", methods=['GET', 'POST'])
def post_variablen_update():
    if request.method == "POST":
        id = request.json.get("id", "")
        type_id = request.json.get("type_id", "")
        key = request.json.get("key", "")
        value = request.json.get("value", "")
        remarks = request.json.get("remarks", "")

        is_key_use = Variablen.where('key', key).first()

        if is_key_use:
            if str(is_key_use.id) != str(id):
                return Response.re(err=ErrVariablenUse)

        Variablen.where('id', id).update(
            {
                "type_id": type_id,
                "key": key,
                "value": value,
                'remarks': remarks,
                "update_time": Time.get_date_time()
            }
        )

        return Response.re()


@r.route("/post/variablen/del", methods=['GET', 'POST'])
def post_variablen_del():
    if request.method == "POST":
        id = request.json.get("id", "")
        Variablen.where('id', id).delete()
        return Response.re()


@r.route("/post/variablen/status", methods=['GET', 'POST'])
def post_variablen_status():
    if request.method == "POST":
        id = request.json.get("id", "")
        status = request.json.get("status", "")

        Variablen.where('id', id).update(
            {
                "status": status,
                "update_time": Time.get_date_time()
            }
        )

        return Response.re()
