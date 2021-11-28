#!/usr/bin/env python
# encoding:utf-8
from . import *


@r.route("/get/workflow/list", methods=['GET', 'POST'])
def get_user_list():
    if request.method == "POST":
        keywords = request.json.get("keywords", "")
        type = request.json.get("type", "0")
        page = request.json.get("page", 1)
        page_count = request.json.get("page_count", 10)

        workflow_list = Workflow.join(
            Users.__table__,
            Workflow.__table__ + '.user_id',
            '=',
            Users.__table__ + '.id'
        ).join(
            Types.__table__,
            Workflow.__table__ + '.type_id',
            '=',
            Types.__table__ + '.id'
        ).select(
            Workflow.__table__ + '.id',
            Workflow.__table__ + '.uuid',
            Workflow.__table__ + ".type_id",
            Workflow.__table__ + '.name',
            Workflow.__table__ + '.update_time',
            Workflow.__table__ + '.create_time',
            Users.__table__ + '.nick_name',
            Types.__table__ + '.name as type_name',
            Workflow.__table__ + '.remarks',
            Workflow.__table__ + '.status',
            Workflow.__table__ + '.timer_app',
            Workflow.__table__ + '.webhook_app',
            Workflow.__table__ + '.input_app',
        )

        if str(type) != "0":
            workflow_list = workflow_list.where(Workflow.__table__ + ".type_id", type)

        if str(keywords) == "":
            workflow_list = workflow_list.order_by(Workflow.__table__ + '.id', 'desc').paginate(page_count, page)
        else:
            workflow_list = workflow_list.where(
                Workflow.__table__ + '.name',
                'like',
                '%{keywords}%'.format(keywords=keywords)
            ).order_by(Workflow.__table__ + '.id', 'desc').paginate(page_count, page)

        return Response.re(data=Page(model=workflow_list).to())


@r.route("/post/workflow/add", methods=['GET', 'POST'])
def post_workflow_add():
    if request.method == "POST":
        type = request.json.get("type", 0)

        uuid = Random.make_uuid()

        token = request.headers.get("token")
        user_id = redis.get(token)

        if type == 0:
            work_name = "未命名 " + Time.get_date_time()

            Workflow.insert({
                'uuid': str(uuid),
                "type_id": 1,
                "user_id": user_id,
                'name': work_name,
                'start_app': "",
                'end_app': "",
                'input_app': "",
                'webhook_app': "",
                'timer_app': "",
                'flow_json': "",
                'flow_data': "",
                'controller_data': "",
                'local_var_data': "none",
                'remarks': "",
                'status': 0,
                'grid_type': "mesh",
                'edge_marker': "block",
                'edge_color': "#ccc",
                'edge_connector': "normal",
                'edge_router': "normal",
                'update_time': Time.get_date_time(),
                'create_time': Time.get_date_time()
            })
        elif type == 1:
            name = request.json.get("name", "")
            remarks = request.json.get("remarks", "")
            start_app = request.json.get("start_app", "")
            end_app = request.json.get("end_app", "")
            input_app = request.json.get("input_app", "")
            webhook_app = request.json.get("webhook_app", "")
            timer_app = request.json.get("timer_app", "")
            flow_json = request.json.get("flow_json", "")
            flow_data = request.json.get("flow_data", "")
            controller_data = request.json.get("controller_data", "")
            local_var_data = request.json.get("local_var_data", "")
            grid_type = request.json.get("grid_type", "")
            edge_marker = request.json.get("edge_marker", "")
            edge_color = request.json.get("edge_color", "")
            edge_connector = request.json.get("edge_connector", "")
            edge_router = request.json.get("edge_router", "")

            Workflow.insert({
                'uuid': str(uuid),
                "type_id": 1,
                "user_id": user_id,
                'name': name,
                'start_app': start_app,
                'end_app': end_app,
                'input_app': input_app,
                'webhook_app': webhook_app,
                'timer_app': timer_app,
                'flow_json': flow_json,
                'flow_data': flow_data,
                'controller_data': controller_data,
                'local_var_data': local_var_data,
                'remarks': remarks,
                'status': 0,
                'grid_type': grid_type,
                'edge_marker': edge_marker,
                'edge_color': edge_color,
                'edge_connector': edge_connector,
                'edge_router': edge_router,
                'update_time': Time.get_date_time(),
                'create_time': Time.get_date_time()
            })

        return Response.re(data={"uuid": uuid})


@r.route("/post/workflow/detail", methods=['GET', 'POST'])
def get_workflow_detail():
    if request.method == "POST":
        uuid = request.json.get("uuid", "")

        workflow_info = Workflow.select(
            'uuid',
            'name',
            'start_app',
            'end_app',
            'input_app',
            'webhook_app',
            'timer_app',
            'flow_json',
            'flow_data',
            'controller_data',
            'type_id',
            'remarks',
            'local_var_data',
            'status',
            'grid_type',
            'edge_marker',
            'edge_color',
            'edge_connector',
            'edge_router',
            'update_time',
            'create_time'
        ).where("uuid", uuid).first()

        return Response.re(data=workflow_info.serialize())


@r.route("/post/workflow/update", methods=['GET', 'POST'])
def post_workflow_update():
    if request.method == "POST":
        uuid = request.json.get("uuid", "")
        name = request.json.get("name", "")
        start_app = request.json.get("start_app", "")
        end_app = request.json.get("end_app", "")
        input_app = request.json.get("input_app", "")
        webhook_app = request.json.get("webhook_app", "")
        timer_app = request.json.get("timer_app", "")
        flow_json = request.json.get("flow_json", "")
        flow_data = request.json.get("flow_data", "")
        controller_data = request.json.get("controller_data", "")
        type_id = request.json.get("type_id", "")
        remarks = request.json.get("remarks", "")
        local_var_data = request.json.get("local_var_data", "")
        grid_type = request.json.get("grid_type", "")
        edge_marker = request.json.get("edge_marker", "")
        edge_color = request.json.get("edge_color", "")
        edge_connector = request.json.get("edge_connector", "")
        edge_router = request.json.get("edge_router", "")

        if str(controller_data) != "{}":
            work_info = Workflow.select("timer_app").where('uuid', uuid).first()

            if work_info:
                if str(work_info.timer_app) == "" or str(work_info.timer_app) == "None" or work_info.timer_app is None:
                    w_timer_app = ""
                else:
                    w_timer_app = work_info.timer_app

                conn = rpyc.connect('localhost', 53124)
                conn.root.exec(uuid, timer_app, w_timer_app, controller_data)
                conn.close()
            else:
                return Response.re(err=ErrIsNotPlayBook)

        Workflow.where('uuid', uuid).update({
            'name': name,
            'start_app': start_app,
            'end_app': end_app,
            'input_app': input_app,
            'webhook_app': webhook_app,
            'timer_app': timer_app,
            'flow_json': flow_json,
            'flow_data': flow_data,
            'controller_data': controller_data,
            'type_id': type_id,
            'remarks': remarks,
            'local_var_data': local_var_data,
            'grid_type': grid_type,
            'edge_marker': edge_marker,
            'edge_color': edge_color,
            'edge_connector': edge_connector,
            'edge_router': edge_router,
            'update_time': Time.get_date_time()
        })

        return Response.re()


@r.route("/post/workflow/del", methods=['GET', 'POST'])
def post_workflow_del():
    if request.method == "POST":
        uuid = request.json.get("uuid", "")

        work_info = Workflow.select("timer_app").where('uuid', uuid).first()

        if work_info:
            if str(work_info.timer_app) == "" or str(work_info.timer_app) == "None" or work_info.timer_app is None:
                pass
            else:
                conn = rpyc.connect('localhost', 53124)
                conn.root.remove(work_info.timer_app)
                conn.close()
        else:
            return Response.re(err=ErrIsNotPlayBook)

        Workflow.where('uuid', uuid).delete()
        return Response.re()


@r.route("/post/workflow/status", methods=['GET', 'POST'])
def post_workflow_status():
    if request.method == "POST":
        id = request.json.get("id", "")
        status = request.json.get("status", "")

        Workflow.where('id', id).update(
            {
                "status": status,
                "update_time": Time.get_date_time()
            }
        )

        return Response.re()


@r.route("/get/workflow/import_url", methods=['GET', 'POST'])
def post_workflow_import_url():
    if request.method == "POST":
        url = request.json.get("url", "")
        try:
            r = requests.get(url=url, timeout=10)
            return Response.re(data={"data": r.json()})
        except:
            return Response.re(err=ErrImportUrl)


@r.route("/get/workflow/statistics", methods=['GET', 'POST'])
def post_workflow_statistics():
    if request.method == "POST":
        url = request.json.get("url", "")
        try:
            r = requests.get(url=url, timeout=10)
            return Response.re(data={"data": r.json()})
        except:
            return Response.re(err=ErrImportUrl)


@ws.route('/echo')
def echo_socket(s):
    while not s.closed:
        message = s.receive()

        if message:
            req_data = json.loads(message)
            method = req_data["method"]

            if method == "ping":
                pass
            elif method == "run":
                uuid = req_data["data"]["uuid"]
                auto_execute(uuid, s=s)


def get_workflow_logs(uuid):
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
    ).where(
        Workflow.__table__ + '.uuid',
        uuid
    ).order_by(
        Workflow.__table__ + '.id',
        'desc'
    ).limit(100).get()

    return logs_list


@r.route("/get/workflow/logs", methods=['GET', 'POST'])
def get_workflow_logs_info():
    if request.method == "POST":
        uuid = request.json.get("uuid", "")
        logs_list = get_workflow_logs(uuid)
        return Response.re(data=logs_list.serialize())


def get_workflow_sums(uuid):
    if redis.exists(uuid + "&&exec_sum") == 1:
        exec_sum = redis.get(uuid + "&&exec_sum")
    else:
        exec_sum = 0

    return exec_sum


@r.route("/get/workflow/sums", methods=['GET', 'POST'])
def get_workflow_sums_info():
    if request.method == "POST":
        uuid = request.json.get("uuid", "")
        exec_sum = get_workflow_sums(uuid)

        data = {
            "exec_sum": exec_sum
        }

        return Response.re(data=data)


def get_workflow_success_fail(uuid):
    sql1 = '''
    SELECT
        COUNT(1) as x 
    FROM
        w5_logs 
    WHERE
        uuid = "{uuid}" 
    GROUP BY
        only_id
    '''.format(uuid=uuid)

    sql2 = '''
    SELECT
        COUNT(1) as x 
    FROM
        w5_logs 
    WHERE
        `status` != 0 
        AND uuid = "{uuid}"
    GROUP BY
        only_id
    '''.format(uuid=uuid)

    r1 = db.select(sql1)
    r2 = db.select(sql2)

    return len(r1), len(r1) - len(r2), len(r2)


@r.route("/get/workflow/workflow", methods=['GET', 'POST'])
def get_workflow_workflow():
    if request.method == "POST":
        uuid = request.json.get("uuid", "")
        sum, success_sum, fail_sum = get_workflow_success_fail(uuid)

        result = [
            {
                "name": "成功",
                "sum": success_sum
            },
            {
                "name": "失败",
                "sum": fail_sum
            }
        ]

        if redis.exists(uuid + "&&exec_sum") == 1:
            exec_sum = redis.get(uuid + "&&exec_sum")
        else:
            exec_sum = 0

        data = {
            "result": result,
            "exec_sum": exec_sum
        }

        return Response.re(data=data)


def get_workflow_exec(uuid):
    sql = '''
        SELECT
            DATE_FORMAT( create_time, '%%m-%%d#%%H' ) AS time,
            count(id) AS value 
        FROM
            {logs} 
        WHERE
            DATE( create_time ) > DATE_SUB( CURDATE(), INTERVAL 1 DAY ) 
        AND uuid="{uuid}"
        GROUP BY
            time;
        '''.format(
        logs=Logs.__table__,
        uuid=uuid
    )

    exec_data = db.select(sql)

    time_data = {}

    for t in Time.get_hour():
        time_data[t] = 0

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

    return result


@r.route("/get/workflow/exec", methods=['GET', 'POST'])
def get_workflow_exec_info():
    if request.method == "POST":
        uuid = request.json.get("uuid", "")
        result = get_workflow_exec(uuid)
        return Response.re(data=result)
