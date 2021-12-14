#!/usr/bin/env python
# encoding:utf-8
from . import *


@r.route("/get/report/list", methods=['GET', 'POST'])
def get_report_list():
    if request.method == "POST":
        keywords = request.json.get("keywords", "")
        page = request.json.get("page", 1)
        page_count = request.json.get("page_count", 10)

        report_list = Report.select(
            Report.__table__ + '.id',
            Report.__table__ + '.report_no',
            Report.__table__ + '.workflow_name',
            Report.__table__ + ".remarks",
            Report.__table__ + '.create_time',
        )

        if str(keywords) == "":
            report_list = report_list.order_by('id', 'desc').paginate(page_count, page)
        else:
            report_list = report_list.where(
                Report.__table__ + '.workflow_name',
                'like',
                '%{keywords}%'.format(keywords=keywords)
            ).or_where(
                Report.__table__ + '.remarks',
                'like',
                '%{keywords}%'.format(keywords=keywords)
            ).or_where(
                Report.__table__ + '.report_no',
                'like',
                '%{keywords}%'.format(keywords=keywords)
            ).order_by('id', 'desc').paginate(page_count, page)

        return Response.re(data=Page(model=report_list).to())


@r.route("/get/report/log", methods=['GET', 'POST'])
def get_report_log():
    if request.method == "POST":
        only_id = request.json.get("only_id", "")

        logs_list = Logs.select(
            'app_uuid',
            'app_name',
            'status',
            'html',
            'args',
            'create_time',
        ).where("only_id", only_id).get()

        result_data = []

        for log in logs_list:
            data = {}
            data['app_uuid'] = log.app_uuid
            data['app_name'] = log.app_name
            data['status'] = log.status
            data['html'] = log.html

            if str(log.args).strip() == "":
                data['args'] = log.args
            else:
                data['args'] = json.loads(log.args)

            data['create_time'] = log.create_time
            result_data.append(data)

        return Response.re(data=result_data)


@r.route("/post/report/del", methods=['GET', 'POST'])
def post_report_del():
    if request.method == "POST":
        id = request.json.get("id", "")
        Report.where('id', id).delete()
        return Response.re()
