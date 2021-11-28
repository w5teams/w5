#!/usr/bin/env python
# encoding:utf-8
from . import *


@r.route("/get/logs/list", methods=['GET', 'POST'])
def get_logs_list():
    if request.method == "POST":
        keywords = request.json.get("keywords", "")
        type = request.json.get("type", "0")
        page = request.json.get("page", 1)
        page_count = request.json.get("page_count", 10)

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
            logs_list = logs_list.order_by('id', 'desc').paginate(page_count, page)
        else:
            logs_list = logs_list.where(
                Logs.__table__ + '.result',
                'like',
                '%{keywords}%'.format(keywords=keywords)
            ).or_where(
                Logs.__table__ + '.app_name',
                'like',
                '%{keywords}%'.format(keywords=keywords)
            ).order_by('id', 'desc').paginate(page_count, page)

        return Response.re(data=Page(model=logs_list).to())


@r.route("/post/logs/del", methods=['GET', 'POST'])
def post_logs_del():
    if request.method == "POST":
        id = request.json.get("id", "")
        Logs.where('id', id).delete()
        return Response.re()
