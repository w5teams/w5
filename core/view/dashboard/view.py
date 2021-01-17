#!/usr/bin/env python
# encoding:utf-8
from . import *


@r.route("/get/dashboard/logs", methods=['GET', 'POST'])
def get_dashboard_logs():
    if request.method == "POST":
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
        ).order_by(
            Workflow.__table__ + '.id',
            'desc'
        ).limit(100).get()

        return Response.re(data=logs_list.serialize())


@r.route("/get/dashboard/sums", methods=['GET', 'POST'])
def get_dashboard_sums():
    if request.method == "POST":
        user_count = Users.count()
        workflow_count = Workflow.count()
        logs_count = Logs.count()
        logs_err_count = Logs.where("status", "!=", 0).count()

        if redis.exists("exec_sum") == 1:
            exec_sum = redis.get("exec_sum")
        else:
            exec_sum = 0

        data = {
            "user_count": user_count,
            "workflow_count": workflow_count,
            "logs_count": logs_count,
            "logs_err_count": logs_err_count,
            "exec_sum": exec_sum
        }

        return Response.re(data=data)


@r.route("/get/dashboard/workflow", methods=['GET', 'POST'])
def get_dashboard_workflow():
    if request.method == "POST":
        sql = '''
            SELECT
                {type}.name AS type,
                sum(1) AS value
            FROM
                {workflow}
            JOIN {type} ON {workflow}.type_id = {type}.id
            GROUP BY
                {type}.name;
            '''.format(
            type=Types.__table__,
            workflow=Workflow.__table__
        )

        workflow_data = db.select(sql)
        return Response.re(data=workflow_data)


@r.route("/get/dashboard/exec", methods=['GET', 'POST'])
def get_dashboard_exec():
    if request.method == "POST":
        sql = '''
            SELECT
                DATE_FORMAT( create_time, '%%m-%%d#%%H' ) AS time,
                count(id) AS value 
            FROM
                {logs} 
            WHERE
                DATE( create_time ) > DATE_SUB( CURDATE(), INTERVAL 1 DAY ) 
            GROUP BY
                time;
            '''.format(
            logs=Logs.__table__
        )

        exec_data = db.select(sql)

        time_data = {
            "00": 0,
            "01": 0,
            "02": 0,
            "03": 0,
            "04": 0,
            "05": 0,
            "06": 0,
            "07": 0,
            "08": 0,
            "09": 0,
            "10": 0,
            "11": 0,
            "12": 0,
            "13": 0,
            "14": 0,
            "15": 0,
            "16": 0,
            "17": 0,
            "18": 0,
            "19": 0,
            "20": 0,
            "21": 0,
            "22": 0,
            "23": 0
        }

        for t in exec_data:
            arr = str(t.time).split("#")
            time_data[arr[1]] = t.value

        result = []

        for t in time_data:
            data = {
                "time": t,
                "value": time_data[t]
            }

            result.append(data)

        return Response.re(data=result)
