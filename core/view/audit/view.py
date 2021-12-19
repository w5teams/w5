#!/usr/bin/env python
# encoding:utf-8
from . import *


@r.route("/get/audit/list", methods=['GET', 'POST'])
def get_audit_list():
    if request.method == "POST":
        keywords = request.json.get("keywords", "")
        type = request.json.get("type", "0")
        page = request.json.get("page", 1)
        page_count = request.json.get("page_count", 10)

        audit_list = Audit.join(
            Workflow.__table__,
            Audit.__table__ + '.workflow_uuid',
            '=',
            Workflow.__table__ + '.uuid'
        ).join(
            Users.__table__,
            Audit.__table__ + '.user_id',
            '=',
            Users.__table__ + '.id'
        ).select(
            Audit.__table__ + '.id',
            Audit.__table__ + '.workflow_uuid',
            Audit.__table__ + '.only_id',
            Audit.__table__ + ".user_id",
            Audit.__table__ + '.audit_app',
            Audit.__table__ + '.start_app',
            Audit.__table__ + '.status',
            Audit.__table__ + '.update_time',
            Audit.__table__ + '.create_time',
            Workflow.__table__ + '.name',
            Users.__table__ + '.nick_name',
            Users.__table__ + '.avatar'
        )

        if str(type) != "all":
            audit_list = audit_list.where(Audit.__table__ + ".status", type)

        if str(keywords) == "":
            audit_list = audit_list.order_by('id', 'desc').paginate(page_count, page)
        else:
            audit_list = audit_list.where(
                'name',
                'like',
                '%{keywords}%'.format(keywords=keywords)
            ).or_where(
                'nick_name',
                'like',
                '%{keywords}%'.format(keywords=keywords)
            ).order_by('id', 'desc').paginate(page_count, page)

        return Response.re(data=Page(model=audit_list).to())


@r.route("/post/audit/update", methods=['GET', 'POST'])
def post_audit_update():
    if request.method == "POST":
        id = request.json.get("id", "")
        status = request.json.get("status", "")
        only_id = request.json.get("only_id", "")
        workflow_uuid = request.json.get("workflow_uuid", "")
        audit_app = request.json.get("audit_app", "")
        start_app = request.json.get("start_app", "")
        user = request.json.get("user", "")

        auto_execute(workflow_uuid, audit_status=status, audit_app=audit_app, start_app=start_app, only_id=only_id,
                     user=user)

        Audit.where('id', id).update(
            {
                "status": status,
                "update_time": Time.get_date_time()
            }
        )

        return Response.re()
