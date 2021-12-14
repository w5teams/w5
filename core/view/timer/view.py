#!/usr/bin/env python
# encoding:utf-8
from . import *


@r.route("/get/timer/list", methods=['GET', 'POST'])
def get_timer_list():
    if request.method == "POST":
        keywords = request.json.get("keywords", "")
        page = request.json.get("page", 1)
        page_count = request.json.get("page_count", 10)

        timer_list = Timer.join(
            Workflow.__table__,
            Timer.__table__ + '.uuid',
            '=',
            Workflow.__table__ + '.uuid'
        ).select(
            Timer.__table__ + '.id',
            Timer.__table__ + '.timer_uuid',
            Timer.__table__ + '.uuid',
            Timer.__table__ + ".type",
            Timer.__table__ + '.interval_type',
            Timer.__table__ + '.time',
            Timer.__table__ + '.start_date',
            Timer.__table__ + '.end_date',
            Timer.__table__ + '.jitter',
            Timer.__table__ + '.status',
            Timer.__table__ + '.update_time',
            Timer.__table__ + '.create_time',
            Workflow.__table__ + '.name'
        )

        if str(keywords) == "":
            timer_list = timer_list.order_by('id', 'desc').paginate(page_count, page)
        else:
            timer_list = timer_list.where(
                Workflow.__table__ + '.name',
                'like',
                '%{keywords}%'.format(keywords=keywords)
            ).order_by('id', 'desc').paginate(page_count, page)

        return Response.re(data=Page(model=timer_list).to())


@r.route("/post/timer/start_pause", methods=['GET', 'POST'])
def post_timer_start_pause():
    if request.method == "POST":
        uuid = request.json.get("uuid", "")
        type = request.json.get("type", "")

        conn = rpyc.connect('localhost', 53124)

        if type == "start":
            if uuid == "all":
                conn.root.resume_all()
            else:
                conn.root.resume(uuid)
        elif type == "pause":
            if uuid == "all":
                conn.root.pause_all()
            else:
                conn.root.pause(uuid)

        conn.close()
        return Response.re()
