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
        type = request.json.get("type", 1)

        result = []

        if type == 1:
            sql = '''
            SELECT
                DATE_FORMAT(create_time, '%%H') AS time,
                count(id) AS value 
            FROM
                {logs} 
            WHERE
                to_days(create_time) = to_days(now())
            GROUP BY
                time;
            '''.format(
                logs=Logs.__table__
            )

            exec_data = db.select(sql)

            time_data = {}

            for t in Time.get_hour():
                time_data[t] = 0

            for t in exec_data:
                time_data[t.time] = t.value

            for t in time_data:
                data = {
                    "time": t,
                    "value": time_data[t]
                }

                result.append(data)
        elif type == 2:
            sql = '''
            SELECT
                DATE_FORMAT(create_time, '%%H') AS time,
                count(id) AS value 
            FROM
                {logs} 
            WHERE
                TO_DAYS(NOW()) - TO_DAYS(create_time) <= 1  
            GROUP BY
                time;
            '''.format(
                logs=Logs.__table__
            )

            exec_data = db.select(sql)

            time_data = {}

            for t in Time.get_hour():
                time_data[t] = 0

            for t in exec_data:
                time_data[t.time] = t.value

            for t in time_data:
                data = {
                    "time": t,
                    "value": time_data[t]
                }

                result.append(data)

        elif type == 3:
            sql = '''
            SELECT
                DATE_FORMAT( create_time, '%%m-%%d' ) AS time,
                count( id ) AS value
            FROM
                {logs}  
            WHERE
                YEARWEEK(date_format(create_time, '%%Y-%%m-%%d')) = YEARWEEK(now()) 
            GROUP BY
                time;
            '''.format(
                logs=Logs.__table__
            )

            exec_data = db.select(sql)

            time_data = {}

            for t in Time.get_week():
                time_data[t] = 0

            for t in exec_data:
                time_data[t.time] = t.value

            for t in time_data:
                data = {
                    "time": t,
                    "value": time_data[t]
                }

                result.append(data)

        elif type == 4:
            sql = '''
            SELECT
                DATE_FORMAT( create_time, '%%m-%%d' ) AS time,
                count( id ) AS value
            FROM
                {logs}
            WHERE
                date_format( create_time, '%%Y-%%m' ) = date_format( now(), '%%Y-%%m' ) 
            GROUP BY
                time
            ORDER BY time;
            '''.format(
                logs=Logs.__table__
            )

            exec_data = db.select(sql)

            time_data = {}

            for t in Time.get_month():
                time_data[t] = 0

            for t in exec_data:
                time_data[t.time] = t.value

            for t in time_data:
                data = {
                    "time": t,
                    "value": time_data[t]
                }

                result.append(data)

        elif type == 5:
            sql = '''
            SELECT
                DATE_FORMAT( create_time, '%%m-%%d' ) AS time,
                count( id ) AS value
            FROM
                {logs}
            WHERE
               date_format( create_time, '%%Y-%%m' ) = date_format(DATE_SUB(curdate(), INTERVAL 1 MONTH),'%%Y-%%m') 
            GROUP BY
                time
            ORDER BY time;
            '''.format(
                logs=Logs.__table__
            )

            exec_data = db.select(sql)

            time_data = {}

            for t in Time.get_upper_month():
                time_data[t] = 0

            for t in exec_data:
                time_data[t.time] = t.value

            for t in time_data:
                data = {
                    "time": t,
                    "value": time_data[t]
                }

                result.append(data)
        elif type == 6:
            sql = '''
            SELECT
                DATE_FORMAT( create_time, '%%m') AS time,
                count( id ) AS value
            FROM
                {logs} 
            WHERE
                YEAR(create_time)=YEAR(NOW())
            GROUP BY
                time
            ORDER BY time;
            '''.format(
                logs=Logs.__table__
            )

            exec_data = db.select(sql)

            time_data = {}

            for t in Time.get_year():
                time_data[t] = 0

            for t in exec_data:
                time_data[t.time] = t.value

            for t in time_data:
                data = {
                    "time": t,
                    "value": time_data[t]
                }

                result.append(data)

        return Response.re(data=result)


@r.route("/get/dashboard/login_history", methods=['GET', 'POST'])
def get_dashboard_login_history():
    if request.method == "POST":
        login_history_list = LoginHistory.join(
            Users.__table__,
            LoginHistory.__table__ + '.user_id',
            '=',
            Users.__table__ + '.id'
        ).select(
            Users.__table__ + '.id',
            Users.__table__ + '.account',
            Users.__table__ + '.nick_name',
            Users.__table__ + '.avatar',
            LoginHistory.__table__ + ".login_time",
        ).order_by(
            LoginHistory.__table__ + '.id',
            'desc'
        ).limit(100).get()

        return Response.re(data=login_history_list.serialize())
