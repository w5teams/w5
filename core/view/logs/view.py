#!/usr/bin/env python
# encoding:utf-8
from . import *


@r.route("/get/logs/list", methods=['GET', 'POST'])
def get_logs_list():
    if request.method == "POST":
        keywords = request.json.get("keywords", "")
        type = request.json.get("type", "0")

        logs_list = Logs.join(
            Workflow.__table__,
            Logs.__table__ + '.uuid',
            '=',
            Workflow.__table__ + '.uuid'
        ).select(
            Logs.__table__ + '.id',
            Logs.__table__ + '.only_id',
            Logs.__table__ + '.uuid',
            Logs.__table__ + ".app_name",
            Logs.__table__ + '.result',
            Logs.__table__ + '.create_time',
            Logs.__table__ + '.status',
            Logs.__table__ + '.args',
            Workflow.__table__ + '.name'
        )

        if str(type) != "0":
            logs_list = logs_list.where(Logs.__table__ + ".uuid", type)

        if str(keywords) == "":
            logs_list = logs_list.order_by('id', 'desc').get()
        else:
            logs_list = logs_list.where(
                Logs.__table__ + '.result',
                'like',
                '%{keywords}%'.format(keywords=keywords)
            ).or_where(
                Logs.__table__ + '.app_name',
                'like',
                '%{keywords}%'.format(keywords=keywords)
            ).order_by('id', 'desc').get()

        return Response.re(data=logs_list.serialize())


@r.route("/post/logs/del", methods=['GET', 'POST'])
def post_logs_del():
    if request.method == "POST":
        id = request.json.get("id", "")
        Logs.where('id', id).delete()
        return Response.re()
