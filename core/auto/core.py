#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3

# 希望您，能提交代码帮助 W5 变得更好，欢迎联系三斤交流

import re
import copy
import json
import asyncio
import threading
import importlib
import traceback
import nest_asyncio
from core import redis
from rpyc import Service
from loguru import logger
from core.utils.file import File
from core.utils.times import Time
from core.utils.randoms import Random
from core import (lose_time, max_instances, w5_apps_path)
from apscheduler.schedulers.gevent import GeventScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.base import JobLookupError
from core.model import (Logs, Workflow, Variablen, Report, Timer, Audit)

nest_asyncio.apply()


class W5Timer(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.scheduler = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(W5Timer, "_instance"):
            with W5Timer._instance_lock:
                if not hasattr(W5Timer, "_instance"):
                    W5Timer._instance = object.__new__(cls)
        return W5Timer._instance

    def create_scheduler(self):
        self.scheduler = GeventScheduler(
            job_defaults={
                'coalesce': False,
                'max_instances': max_instances
            }
        )

    def start(self):
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()

    def pause(self, uuid):
        self.scheduler.pause_job(uuid)

    def pause_all(self):
        self.scheduler.pause()

    def resume(self, uuid):
        self.scheduler.resume_job(uuid)

    def resume_all(self):
        self.scheduler.resume()

    def remove_job(self, uuid):
        try:
            self.scheduler.remove_job(uuid)
        except JobLookupError:
            pass

    def get_jobs(self):
        return self.scheduler.get_jobs()

    def add_date(self, run_date=None, uuid=None, timer_uuid=None):
        self.scheduler.add_job(
            auto_execute,
            'date',
            run_date=run_date,
            id=timer_uuid,
            args=(uuid,)
        )

    def update_date(self, uuid, run_date=None):
        self.scheduler.reschedule_job(
            uuid,
            trigger='date',
            run_date=run_date
        )

    def add_interval(self, t, interval, uuid=None, timer_uuid=None, start_date=None, end_date=None, jitter=0):
        if t == "seconds":
            self.scheduler.add_job(
                auto_execute,
                'interval',
                seconds=interval,
                start_date=start_date,
                end_date=end_date,
                jitter=jitter,
                id=timer_uuid,
                args=(uuid,)
            )
        elif t == "minutes":
            self.scheduler.add_job(
                auto_execute,
                'interval',
                minutes=interval,
                start_date=start_date,
                end_date=end_date,
                jitter=jitter,
                id=timer_uuid,
                args=(uuid,)
            )
        elif t == "hours":
            self.scheduler.add_job(
                auto_execute,
                'interval',
                hours=interval,
                start_date=start_date,
                end_date=end_date,
                jitter=jitter,
                id=timer_uuid,
                args=(uuid,)
            )
        elif t == "days":
            self.scheduler.add_job(
                auto_execute,
                'interval',
                days=interval,
                start_date=start_date,
                end_date=end_date,
                jitter=jitter,
                id=timer_uuid,
                args=(uuid,)
            )
        elif t == "weeks":
            self.scheduler.add_job(
                auto_execute,
                'interval',
                weeks=interval,
                start_date=start_date,
                end_date=end_date,
                jitter=jitter,
                id=timer_uuid,
                args=(uuid,)
            )

    def update_interval(self, uuid, t, interval, start_date=None, end_date=None, jitter=0):
        if t == "seconds":
            self.scheduler.reschedule_job(
                uuid,
                trigger="interval",
                seconds=interval,
                start_date=start_date,
                end_date=end_date,
                jitter=jitter
            )
        elif t == "minutes":
            self.scheduler.reschedule_job(
                uuid,
                trigger="interval",
                minutes=interval,
                start_date=start_date,
                end_date=end_date,
                jitter=jitter
            )
        elif t == "hours":
            self.scheduler.reschedule_job(
                uuid,
                trigger="interval",
                hours=interval,
                start_date=start_date,
                end_date=end_date,
                jitter=jitter
            )
        elif t == "days":
            self.scheduler.reschedule_job(
                uuid,
                trigger="interval",
                days=interval,
                start_date=start_date,
                end_date=end_date,
                jitter=jitter
            )
        elif t == "weeks":
            self.scheduler.reschedule_job(
                uuid,
                trigger="interval",
                weeks=interval,
                start_date=start_date,
                end_date=end_date,
                jitter=jitter
            )

    def add_cron(self, cron, uuid=None, timer_uuid=None, start_date=None, end_date=None, jitter=0):
        self.scheduler.add_job(
            auto_execute,
            CronTrigger.from_crontab(cron),
            start_date=start_date,
            end_date=end_date,
            jitter=jitter,
            id=timer_uuid,
            args=(uuid,)
        )

    def update_cron(self, uuid, cron, start_date=None, end_date=None, jitter=0):
        values = cron.split()

        if len(values) != 5:
            raise ValueError('Wrong number of fields; got {}, expected 5'.format(len(values)))

        self.scheduler.reschedule_job(
            uuid,
            None,
            "cron",
            minute=values[0],
            hour=values[1],
            day=values[2],
            month=values[3],
            day_of_week=values[4],
            start_date=start_date,
            end_date=end_date,
            jitter=jitter
        )


w5_timer = W5Timer()


class ManageTimer(Service):
    def __init__(self):
        self.uuid = None
        self.timer_app = None
        self.w_timer_app = None
        self.controller_data = None
        self.config = {}

    def load_config(self):
        controller_data = json.loads(self.controller_data)[self.timer_app]
        type = controller_data["type"]

        if "interval_type" in controller_data:
            interval_type = controller_data["interval_type"]
        else:
            interval_type = ""

        time = controller_data["time"]

        if "start_date" in controller_data:
            start_date = controller_data["start_date"]
            start_date_x = controller_data["start_date"]
        else:
            start_date = ""
            start_date_x = None

        if "end_date" in controller_data:
            end_date = controller_data["end_date"]
            end_date_x = controller_data["end_date"]
        else:
            end_date = ""
            end_date_x = None

        if "jitter" in controller_data:
            jitter = int(controller_data["jitter"])
        else:
            jitter = 0

        self.config["type"] = type
        self.config["interval_type"] = interval_type
        self.config["time"] = time
        self.config["start_date"] = start_date
        self.config["start_date_x"] = start_date_x
        self.config["end_date"] = end_date
        self.config["end_date_x"] = end_date_x
        self.config["jitter"] = jitter

    def exposed_remove(self, timer_app=None):
        if timer_app:
            Timer.where('timer_uuid', timer_app).delete()
            w5_timer.remove_job(timer_app)
        else:
            Timer.where('timer_uuid', self.w_timer_app).delete()
            w5_timer.remove_job(self.w_timer_app)

    def exposed_pause(self, uuid=None):
        if uuid:
            w5_timer.pause(uuid=uuid)

            Timer.where('timer_uuid', uuid).update({
                'status': 0,
                'update_time': Time.get_date_time()
            })
        else:
            w5_timer.pause(uuid=self.w_timer_app)

            Timer.where('timer_uuid', self.w_timer_app).update({
                'status': 0,
                'update_time': Time.get_date_time()
            })

    def exposed_resume(self, uuid=None):
        if uuid:
            w5_timer.resume(uuid=uuid)

            Timer.where('timer_uuid', uuid).update({
                'status': 1,
                'update_time': Time.get_date_time()
            })
        else:
            w5_timer.resume(uuid=self.w_timer_app)

            Timer.where('timer_uuid', self.w_timer_app).update({
                'status': 1,
                'update_time': Time.get_date_time()
            })

    def start(self):
        w5_timer.create_scheduler()
        w5_timer.start()

        timer_list = Timer.select("timer_uuid", "uuid", "type", "interval_type", "time", "start_date", "end_date",
                                  "jitter",
                                  "status").get()

        count = 0

        for t in timer_list:
            if count == 0:
                logger.info("============== 任务调度恢复中 =================")

            if t.start_date == "":
                t.start_date = None

            if t.end_date == "":
                t.end_date = None

            if t.type == "date":
                w5_timer.add_date(run_date=t.time, uuid=t.uuid, timer_uuid=t.timer_uuid)
            elif t.type == "interval":
                w5_timer.add_interval(t.interval_type, int(t.time), uuid=t.uuid,
                                      timer_uuid=t.timer_uuid,
                                      start_date=t.start_date,
                                      end_date=t.end_date,
                                      jitter=t.jitter)
            elif t.type == "cron":
                w5_timer.add_cron(t.time, uuid=t.uuid, timer_uuid=t.timer_uuid,
                                  start_date=t.start_date,
                                  end_date=t.end_date,
                                  jitter=t.jitter)

            if str(t.status) == "0":
                w5_timer.pause(t.timer_uuid)

            logger.info(
                "{timer_uuid} {type} {time}",
                timer_uuid=t.timer_uuid,
                type=t.type,
                time=t.time
            )

            count = count + 1

        if count > 0:
            logger.info("============== 任务调度恢复完成 =================")

    def exposed_pause_all(self):
        w5_timer.pause_all()

        Timer.where("id", "!=", "0").update({
            'status': 0,
            'update_time': Time.get_date_time()
        })

    def exposed_resume_all(self):
        w5_timer.resume_all()

        Timer.where("id", "!=", "0").update({
            'status': 1,
            'update_time': Time.get_date_time()
        })

    def exposed_get_jobs(self):
        return w5_timer.get_jobs()

    def add_timer(self):
        self.load_config()

        if self.config["type"] == "date":
            w5_timer.add_date(run_date=self.config["time"], uuid=self.uuid, timer_uuid=self.timer_app)
        elif self.config["type"] == "interval":
            w5_timer.add_interval(self.config["interval_type"], int(self.config["time"]), uuid=self.uuid,
                                  timer_uuid=self.timer_app,
                                  start_date=self.config["start_date_x"],
                                  end_date=self.config["end_date_x"],
                                  jitter=self.config["jitter"])
        elif self.config["type"] == "cron":
            w5_timer.add_cron(self.config["time"], uuid=self.uuid, timer_uuid=self.timer_app,
                              start_date=self.config["start_date_x"],
                              end_date=self.config["end_date_x"],
                              jitter=self.config["jitter"])

        w5_timer.pause(self.timer_app)

        Timer.insert({
            'timer_uuid': self.timer_app,
            'uuid': self.uuid,
            "type": self.config["type"],
            'interval_type': self.config["interval_type"],
            'time': self.config["time"],
            'start_date': self.config["start_date"],
            'end_date': self.config["end_date"],
            'jitter': self.config["jitter"],
            'status': 0,
            'update_time': Time.get_date_time(),
            'create_time': Time.get_date_time()
        })

    def update_timer(self):
        self.load_config()

        if self.config["type"] == "date":
            try:
                w5_timer.update_date(self.timer_app, self.config["time"])
            except:
                w5_timer.add_date(run_date=self.config["time"], uuid=self.uuid, timer_uuid=self.timer_app)
        elif self.config["type"] == "interval":
            try:
                w5_timer.update_interval(self.timer_app, self.config["interval_type"], int(self.config["time"]),
                                         start_date=self.config["start_date_x"],
                                         end_date=self.config["end_date_x"],
                                         jitter=self.config["jitter"])
            except:
                w5_timer.add_interval(self.config["interval_type"], int(self.config["time"]), uuid=self.uuid,
                                      timer_uuid=self.timer_app,
                                      start_date=self.config["start_date_x"],
                                      end_date=self.config["end_date_x"],
                                      jitter=self.config["jitter"])
        elif self.config["type"] == "cron":
            try:
                w5_timer.update_cron(self.timer_app, self.config["time"], start_date=self.config["start_date_x"],
                                     end_date=self.config["end_date_x"],
                                     jitter=self.config["jitter"])
            except:
                w5_timer.add_cron(self.config["time"], uuid=self.uuid, timer_uuid=self.timer_app,
                                  start_date=self.config["start_date_x"],
                                  end_date=self.config["end_date_x"],
                                  jitter=self.config["jitter"])

        Timer.where('timer_uuid', self.timer_app).update({
            "type": self.config["type"],
            'interval_type': self.config["interval_type"],
            'time': self.config["time"],
            'start_date': self.config["start_date"],
            'end_date': self.config["end_date"],
            'jitter': self.config["jitter"],
            'update_time': Time.get_date_time()
        })

    def exposed_exec(self, uuid=None, timer_app=None, w_timer_app=None, controller_data=None):
        self.uuid = uuid
        self.timer_app = timer_app
        self.w_timer_app = w_timer_app
        self.controller_data = controller_data

        if self.timer_app == "" and str(self.w_timer_app) != "":
            self.exposed_remove()
        elif self.timer_app != "" and str(self.w_timer_app) != "":
            if self.timer_app == self.w_timer_app:
                timer_info = Timer.select("timer_uuid").where('timer_uuid', self.timer_app).first()
                if timer_info:
                    self.update_timer()
                else:
                    self.add_timer()
            else:
                self.exposed_remove()
                self.add_timer()
        elif self.timer_app != "" and str(self.w_timer_app) == "":
            self.add_timer()


class W5Tree(object):
    def __init__(self):
        pass

    async def make_format(self, datas, start):
        result = []
        for i in datas:
            d = {
                "left": i[0],
                "right": i[1]
            }

            result.append(d)

        result.append({"right": start})

        return result

    async def make_tree(self, datas):
        result = {}
        for d in datas:
            d.setdefault("left", "")
            result.setdefault(d['left'], {})
            result.setdefault(d['right'], {})
            result[d['left']][d['right']] = result[d['right']]

        return result[""]

    async def make_path(self, root, end):
        result = []

        def echo(root, path, end):
            if path.split("->")[-1:][0] == end:
                result.append(path)
            if root == {}:
                return
            key = list(root.keys())
            for k in key:
                if path == "":
                    echo(root[k], path + k, end)
                else:
                    echo(root[k], path + "->" + k, end)

        echo(root, "", end)

        return result

    async def get_paths(self, d, start, end):
        data = await self.make_format(datas=d, start=start)
        tree = await self.make_tree(datas=data)
        result = await self.make_path(root=tree, end=end)
        return result


class Auto(object):
    def __init__(self, socket=None):
        self.only_id = Random.make_order_number(length=10)
        self.workflow_name = None
        self.workflow_remarks = None
        self.socket = socket
        self.flow_json = None
        self.flow_data = None
        self.local_var_data = None
        self.global_var_data = None
        self.start_app = None
        self.end_app = None
        self.input_app = None
        self.webhook_app = None
        self.timer_app = None
        self.for_list = None
        self.if_list = None
        self.audit_list = None
        self.node_link_data = None
        self.node_name_list = None
        self.local_var_data = None
        self.controller_data = None

    def is_json(self, json_text):
        try:
            int(json_text)
            return False
        except Exception:
            try:
                json.dumps("{'errcode': 300001, 'errmsg': 'token is not exist'}")
                json.loads(json_text)
            except ValueError:
                return False
            except TypeError:
                return True

            return True

    async def is_identification(self, app_dir):
        app_json = File.find_app_json(path=w5_apps_path, app_dir=app_dir)
        app_json_load = json.loads(app_json)

        if "identification" in app_json_load:
            if app_json_load["identification"] == "w5soar":
                return True

        return False

    async def is_public(self, app_dir):
        app_json = File.find_app_json(path=w5_apps_path, app_dir=app_dir)
        app_json_load = json.loads(app_json)

        if "is_public" in app_json_load:
            return 1, app_json_load["is_public"]

        return 0, False

    async def make_var(self, local_var, controller_var):
        if controller_var == "none" or str(controller_var).replace(" ", "") == "" or str(controller_var).replace(" ",
                                                                                                                 "") == "{}":
            pass
        else:
            controller_var = json.loads(controller_var)

            for x in controller_var:
                if x != self.timer_app:
                    if x in self.for_list or x in self.if_list:
                        key = x + "&&" + self.only_id + "&&action"
                        redis.set(key, controller_var[x]["action"], ex=lose_time)

                    try:
                        key = x + "&&" + self.only_id + "&&text"
                        redis.set(key, controller_var[x]["text"], ex=lose_time)
                    except:
                        pass

        if local_var == "none" or str(local_var).replace(" ", "") == "" or str(local_var).replace(" ", "") == "[]":
            pass
        else:
            local_var = json.loads(local_var)
            local_var_data = {}

            for x in local_var:
                local_var_data[x["key"]] = x["value"]

            if len(local_var_data) > 0:
                self.local_var_data = local_var_data

        global_var_data = {}

        global_var_list = Variablen.select('key', 'value').where("status", 0).get()

        for x in global_var_list:
            global_var_data[str(x.key)] = str(x.value)

        if len(global_var_data) > 0:
            self.global_var_data = global_var_data

    async def analysis_var(self, text):
        global_var = re.findall(r'@\{\w*\}', text)
        local_var = re.findall(r'@\[\w*\]', text)
        app_var = re.findall(r'@\(\w*-\w*-\w*-\w*-\w*.\w.*?\)', text)

        if len(local_var) > 0:
            if self.local_var_data is None:
                return 1, "请添加局部变量"

        if len(global_var) > 0:
            if self.global_var_data is None:
                return 1, "请添加全局变量"

        for r in set(local_var):
            local_key = str(r).replace("@[", "").replace("]", "")

            try:
                local_value = self.local_var_data[local_key]
            except:
                return 1, "未找到局部变量"
            else:
                text = text.replace(r, local_value)

        for r in set(global_var):
            global_key = str(r).replace("@{", "").replace("}", "")

            try:
                global_value = self.global_var_data[global_key]
            except:
                return 1, "未找到全局变量"
            else:
                text = text.replace(r, global_value)

        for r in set(app_var):
            app_key = str(r).replace("@(", "").replace(")", "").split(".")

            try:
                app_key_json = app_key[1].split("!>")
                redis_key = app_key[0] + "&&" + self.only_id + "&&" + str(app_key_json[0])
                app_value = redis.get(redis_key).decode()

                if len(app_key_json) > 1:
                    is_json = self.is_json(json_text=app_value)

                    if is_json is False:
                        return 1, "非 JSON 格式变量"

                    try:
                        app_value = json.loads(json.loads(app_value))
                    except:
                        app_value = json.loads(app_value)

                    key_all = "app_value"
                    key_front = "['"
                    key_after = "']"
                    key_number_front = "["
                    key_number_after = "]"

                    json_key = ""

                    for k in app_key_json[1:]:
                        try:
                            int(k)
                            key_all += key_number_front + k + key_number_after
                            json_key = json_key + "," + str(k)
                        except ValueError:
                            k = str(k).replace("!!!", "")
                            key_all += key_front + k + key_after
                            json_key = json_key + "," + str(k)
                    try:
                        app_value = eval(key_all)
                    except IndexError:
                        return 1, "未找到 JSON Index : {key}".format(key=json_key[1:])
                    except KeyError:
                        return 1, "未找到 JSON KEY : {key}".format(key=json_key[1:])
            except Exception as e:
                return 1, "未找到 APP 变量"
            else:
                text = text.replace(r, str(app_value))

        return 0, text

    async def add_execute_logs(self, uuid, app_uuid, app_name, result, status, html, args=""):
        try:
            # 更改 Unicode 为 UTF-8 中文
            is_unicode = re.findall(r'\\u\w\w*', str(result))

            if len(is_unicode) > 0:
                result = str(result).encode('utf-8').decode("unicode_escape")
                html = str(html).encode('utf-8').decode("unicode_escape")
        except:
            pass

        log_info = {
            'only_id': self.only_id,
            'uuid': uuid,
            'app_uuid': app_uuid,
            'app_name': app_name,
            'result': result,
            'status': status,
            'html': html,
            'args': args,
            'create_time': Time.get_date_time()
        }

        Logs.insert(log_info)

        logger.info(
            "{only_id} {uuid} {app_uuid} {app_name} {result} {status} {create_time}",
            only_id=self.only_id,
            uuid=uuid,
            app_uuid=app_uuid,
            app_name=app_name,
            result=result,
            status=status,
            create_time=log_info["create_time"]
        )

        data = {
            "method": "execute_log",
            "data": log_info
        }

        if self.socket is None:
            pass
        else:
            try:
                self.socket.send(json.dumps(data))
            except:
                pass

    async def add_report(self):
        report_info = {
            'report_no': self.only_id,
            'workflow_name': self.workflow_name,
            'remarks': self.workflow_remarks,
            'create_time': Time.get_date_time()
        }

        Report.insert(report_info)

    async def add_audit(self, workflow_uuid, only_id, user_id, audit_app, start_app):
        datetime = Time.get_date_time()

        report_info = {
            'workflow_uuid': workflow_uuid,
            'only_id': only_id,
            'user_id': user_id,
            'audit_app': audit_app,
            'start_app': start_app,
            'status': 0,
            'update_time': datetime,
            'create_time': datetime
        }

        Audit.insert(report_info)

    async def execute(self, app_uuid, app_dir=None, datas=None):
        args_data = copy.deepcopy(datas)

        if app_dir:
            args_data["app_dir"] = app_dir

        args_data_json_x = json.dumps(args_data)

        if self.input_app == app_uuid or self.webhook_app == app_uuid:
            key = app_uuid + "&&" + self.only_id + "&&text"
            return {"status": 0, "result": redis.get(key).decode(), "args": args_data_json_x, "html": ""}

        if self.timer_app == app_uuid:
            result_text = "[通知消息] 定时器执行中..."
            return {"status": 0, "result": result_text, "args": args_data_json_x, "html": result_text}

        is_identification = await self.is_identification(app_dir=app_dir)

        if is_identification == False:
            result_text = "[配置错误] 请配置 is_identification"
            return {"status": 2, "result": result_text, "args": args_data_json_x, "html": result_text}

        is_public_status, is_public = await self.is_public(app_dir=app_dir)

        if is_public_status == 0:
            result_text = "[配置错误] 请配置 is_public"
            return {"status": 2, "result": result_text, "args": args_data_json_x, "html": result_text}

        # import_path = ""

        # if platform.system() == 'Windows':
        #     import_path = 'apps.' + str(app_dir) + '.windows.run'
        # elif platform.system() == 'Linux':
        #     import_path = 'apps.' + str(app_dir) + '.linux.run'
        # elif platform.system() == "Darwin":
        #     import_path = 'apps.' + str(app_dir) + '.mac.run'

        import_path = 'apps.' + str(app_dir) + '.main.run'

        try:
            datas["app"] = importlib.import_module(import_path)
            app_action = getattr(datas["app"], datas["action"])
        except Exception as e:
            logger.error("{node_name} {action} {err}".format(
                node_name=datas["node_name"],
                action=datas["action"],
                err=traceback.format_exc())
            )
            result_text = "[程序错误] " + str(e)
            return {"status": 2, "result": result_text, "args": args_data_json_x, "html": result_text}

        args = ""

        for key in datas:
            if key != "node_name" and key != "action" and key != "app" and key != "action_name" and key != "description" and key != "app_dir":
                args = args + "," + key

                var_status, text = await self.analysis_var(text=str(datas[key]))

                redis_key = app_uuid + "&&" + self.only_id + "&&" + key
                redis.set(redis_key, text, ex=lose_time)

                if var_status == 0:
                    datas[key] = text
                    args_data[key] = text
                else:
                    return {"status": var_status, "result": text, "args": args_data_json_x, "html": ""}

        args_data_json = json.dumps(args_data)

        try:
            kwargs = {}
            for arg in args[1:].split(","):
                if arg in datas:
                    kwargs[arg] = datas[arg]
            result_data = await app_action(**kwargs)
        except TypeError as e:
            logger.error("{node_name} {action} {err}".format(
                node_name=datas["node_name"],
                action=datas["action"],
                err=traceback.format_exc())
            )
            result_text = "[非法应用] " + str(e)
            return {"status": 2, "result": result_text, "args": args_data_json, "html": result_text}
        except Exception as e:
            logger.error("{node_name} {action} {err}".format(
                node_name=datas["node_name"],
                action=datas["action"],
                err=traceback.format_exc())
            )
            result_text = "[未知错误] " + str(e)
            return {"status": 2, "result": result_text, "args": args_data_json, "html": result_text}

        if "status" not in result_data:
            result_text = "[返回错误] 请检测 status 返回字段"
            return {"status": 2, "result": result_text, "args": args_data_json, "html": result_text}

        if "result" not in result_data:
            result_text = "[返回错误] 请检测 result 返回字段"
            return {"status": 2, "result": result_text, "args": args_data_json, "html": result_text}

        if "html" not in result_data:
            html_data = ""
        else:
            html_data = result_data["html"]

        return {"status": result_data["status"], "result": result_data["result"], "args": args_data_json,
                "html": html_data}

    async def get_app_data(self, uuid, app_uuid, app_info=None, for_play=False):
        key_result = app_uuid + "&&" + self.only_id + "&&result"
        key_status = app_uuid + "&&" + self.only_id + "&&status"

        if self.input_app == app_uuid or self.webhook_app == app_uuid or self.timer_app == app_uuid:
            if redis.exists(key_result) == 0:
                result_data = await self.execute(app_uuid=app_uuid)

                is_json = self.is_json(json_text=result_data["result"])

                if is_json:
                    result = json.dumps(result_data["result"], ensure_ascii=False)
                else:
                    result = str(result_data["result"])

                redis.set(key_result, result, ex=lose_time)
                redis.set(key_status, result_data["status"], ex=lose_time)

                if self.input_app == app_uuid:
                    await self.add_execute_logs(uuid=uuid, app_uuid=app_uuid, app_name="用户输入",
                                                result=result, status=result_data["status"], html=result)
                elif self.webhook_app == app_uuid:
                    await self.add_execute_logs(uuid=uuid, app_uuid=app_uuid, app_name="WebHook",
                                                result=result, status=result_data["status"],
                                                html=result)
                elif self.timer_app == app_uuid:
                    await self.add_execute_logs(uuid=uuid, app_uuid=app_uuid, app_name="定时器",
                                                result=result, status=result_data["status"],
                                                html=result)

                return result_data["status"], result
            else:
                return int(redis.get(key_status).decode()), redis.get(key_result).decode()
        else:
            try:
                if app_info.get("data").get("app"):
                    del app_info["data"]["app"]
            except:
                pass

            if for_play:
                result_data = await self.execute(app_uuid=app_uuid, app_dir=app_info["app_dir"],
                                                 datas=app_info["data"])

                is_json = self.is_json(json_text=result_data["result"])

                if is_json:
                    result = json.dumps(result_data["result"])
                else:
                    result = str(result_data["result"])

                redis.set(key_result, result, ex=lose_time)
                redis.set(key_status, result_data["status"], ex=lose_time)

                if str(result_data["html"]) == "":
                    html_data = result
                else:
                    html_data = result_data["html"]

                await self.add_execute_logs(
                    uuid=uuid,
                    app_uuid=app_uuid,
                    app_name=app_info["data"]["node_name"],
                    result=result,
                    status=result_data["status"],
                    html=html_data,
                    args=result_data["args"]
                )

                return result_data["status"], result
            else:
                if redis.exists(key_result) == 0:
                    result_data = await self.execute(app_uuid=app_uuid, app_dir=app_info["app_dir"],
                                                     datas=app_info["data"])

                    is_json = self.is_json(json_text=result_data["result"])

                    if is_json:
                        result = json.dumps(result_data["result"])
                    else:
                        result = str(result_data["result"])

                    redis.set(key_result, result, ex=lose_time)
                    redis.set(key_status, result_data["status"], ex=lose_time)

                    if str(result_data["html"]) == "":
                        html_data = result
                    else:
                        html_data = result_data["html"]

                    await self.add_execute_logs(
                        uuid=uuid,
                        app_uuid=app_uuid,
                        app_name=app_info["data"]["node_name"],
                        result=result,
                        status=result_data["status"],
                        html=html_data,
                        args=result_data["args"]
                    )

                    return result_data["status"], result
                else:
                    return int(redis.get(key_status).decode()), redis.get(key_result).decode()

    async def for_play_book(self, paths, uuid, for_play=False):
        for path in paths:
            node_list = str(path).split("->")
            for node_i in range(len(node_list)):
                if node_list[node_i] not in [self.start_app] and node_i > 0:
                    left = node_list[node_i - 1]
                    right = node_list[node_i]

                    if left not in [self.start_app]:
                        if left in self.for_list:
                            paths = await W5Tree().get_paths(d=self.node_link_data, start=right, end=self.end_app)
                            app_name = json.loads(self.controller_data)[left]["node_name"]

                            try:
                                action = redis.get(left + "&&" + self.only_id + "&&action").decode()
                                text = redis.get(left + "&&" + self.only_id + "&&text").decode()
                            except:
                                result_text = "[配置错误] 请配置 FOR 控制器"
                                await self.add_execute_logs(uuid=uuid, app_uuid=left, app_name=app_name,
                                                            result=result_text,
                                                            status=1,
                                                            html="<span>" + result_text + "</span>")
                                raise "请配置 FOR 控制器"

                            var_status, var_text = await self.analysis_var(text=str(text))

                            if var_status != 0:
                                result_text = "[变量错误] " + var_text
                                await self.add_execute_logs(uuid=uuid, app_uuid=left, app_name=app_name,
                                                            result=result_text,
                                                            status=1,
                                                            html="<span>" + result_text + "</span>")
                                raise result_text

                            if action == "1":
                                try:
                                    data = eval(var_text)
                                except:
                                    result_text = "[配置错误] 请输入数组进行循环"
                                    await self.add_execute_logs(uuid=uuid, app_uuid=left, app_name=app_name,
                                                                result=result_text,
                                                                status=1,
                                                                html="<span>" + result_text + "</span>")
                                    raise "请输入数组进行循环"

                                if type(data) != list:
                                    try:
                                        data = eval(data)
                                    except:
                                        result_text = "[配置错误] 请输入数组进行循环"
                                        await self.add_execute_logs(uuid=uuid, app_uuid=left, app_name=app_name,
                                                                    result=result_text,
                                                                    status=1,
                                                                    html="<span>" + result_text + "</span>")
                                        raise "请输入数组进行循环"

                                if type(data) != list:
                                    result_text = "[配置错误] 请输入数组进行循环"
                                    await self.add_execute_logs(uuid=uuid, app_uuid=left, app_name=app_name,
                                                                result=result_text,
                                                                status=1,
                                                                html="<span>" + result_text + "</span>")
                                    raise "请输入数组进行循环"

                                for value in data:

                                    if type(value) == dict:
                                        value = json.dumps(value)
                                    if type(value) == list:
                                        value = json.dumps(value)

                                    redis.set(left + "&&" + self.only_id + "&&value", value, ex=lose_time)
                                    await self.for_play_book(paths=paths, uuid=uuid, for_play=True)

                            elif action == "2":
                                try:
                                    data = eval(var_text)
                                except:
                                    result_text = "[配置错误] 请输入字典进行循环"
                                    await self.add_execute_logs(uuid=uuid, app_uuid=left, app_name=app_name,
                                                                result=result_text,
                                                                status=1,
                                                                html="<span>" + result_text + "</span>")
                                    raise "请输入字典进行循环"

                                if type(data) != dict:
                                    try:
                                        data = eval(data)
                                    except:
                                        result_text = "[配置错误] 请输入字典进行循环"
                                        await self.add_execute_logs(uuid=uuid, app_uuid=left, app_name=app_name,
                                                                    result=result_text,
                                                                    status=1,
                                                                    html="<span>" + result_text + "</span>")
                                        raise "请输入字典进行循环"

                                if type(data) != dict:
                                    result_text = "[配置错误] 请输入字典进行循环"
                                    await self.add_execute_logs(uuid=uuid, app_uuid=left, app_name=app_name,
                                                                result=result_text,
                                                                status=1,
                                                                html="<span>" + result_text + "</span>")
                                    raise "请输入字典进行循环"

                                for key in data:
                                    redis.set(left + "&&" + self.only_id + "&&key", key, ex=lose_time)

                                    result = data[key]

                                    if type(result) == dict:
                                        result = json.dumps(result)
                                    if type(result) == list:
                                        result = json.dumps(result)

                                    redis.set(left + "&&" + self.only_id + "&&value", result, ex=lose_time)
                                    await self.for_play_book(paths=paths, uuid=uuid, for_play=True)
                            elif action == "3":
                                try:
                                    data = int(var_text)
                                except:
                                    result_text = "[配置错误] 请输入数字次数进行循环"
                                    await self.add_execute_logs(uuid=uuid, app_uuid=left, app_name=app_name,
                                                                result=result_text,
                                                                status=1,
                                                                html="<span>" + result_text + "</span>")
                                    raise "请输入数字次数进行循环"

                                if type(data) != int:
                                    result_text = "[配置错误] 请输入数字次数进行循环"
                                    await self.add_execute_logs(uuid=uuid, app_uuid=left, app_name=app_name,
                                                                result=result_text,
                                                                status=1,
                                                                html="<span>" + result_text + "</span>")
                                    raise "请输入数字次数进行循环"

                                for value in range(data):
                                    redis.set(left + "&&" + self.only_id + "&&value", value, ex=lose_time)
                                    await self.for_play_book(paths=paths, uuid=uuid, for_play=True)

                            break
                        if left in self.if_list:
                            if_else_result = redis.get(self.only_id + "if_else_result").decode()

                            is_run = await self.is_condition(
                                left=left,
                                uuid=uuid,
                                if_else_result=if_else_result
                            )

                            if is_run == False:
                                break

                        if left in self.audit_list:
                            user_id = redis.get(left + "&&" + self.only_id + "&&text").decode()
                            await self.add_audit(uuid, self.only_id, user_id, left, right)
                            app_name = json.loads(self.controller_data)[left]["node_name"]
                            await self.add_execute_logs(uuid=uuid, app_uuid=left, app_name=app_name,
                                                        result="剧本等待审核...",
                                                        status=0, html="<span>剧本等待审核...</span>")
                            return 1
                        else:
                            if left in self.if_list:
                                pass
                            else:
                                flow_data_deep = copy.deepcopy(self.flow_data)

                                is_status, if_else_result = await self.get_app_data(
                                    uuid=uuid,
                                    app_uuid=left,
                                    app_info=flow_data_deep.get(left),
                                    for_play=for_play
                                )

                                redis.set(self.only_id + "if_else_result", if_else_result, ex=lose_time)

                                if is_status == 2:
                                    break

        return 0

    async def make_node_link(self, edges):
        link_list = []

        for r in edges:
            if r["shape"] == "w5Edge":
                arr = [r["source"]["cell"], r["target"]["cell"]]
                link_list.append(arr)

        return link_list

    async def make_node_list(self, edges, end_app=None):
        node_list = {}

        for r in edges:
            if r["shape"] == "w5Edge":
                if str(r["source"]["cell"]) != end_app:
                    if node_list.get(r["source"]["cell"]) == None:
                        node_list[r["source"]["cell"]] = 1
                    else:
                        node_list[r["source"]["cell"]] = node_list[r["source"]["cell"]] + 1

        return node_list

    async def make_node_name(self, edges):
        node_list = {}

        for r in edges:
            if r["shape"] == "html":
                node_list[r["id"]] = r["data"]["name"]

        return node_list

    async def is_condition(self, left, uuid, if_else_result):
        try:
            edge_action = redis.get(left + "&&" + self.only_id + "&&action").decode()
            edge_if_else = redis.get(left + "&&" + self.only_id + "&&text").decode()
            var_status, edge_if_else = await self.analysis_var(text=str(edge_if_else))

            if var_status != 0:
                await self.add_execute_logs(
                    uuid=uuid, app_uuid="", app_name="",
                    result=edge_if_else,
                    status=1,
                    html="<span>{result}</span>".format(result=edge_if_else))

                raise

        except Exception as e:
            result_text = "[条件错误] 当前剧本不具备可执行条件 " + str(e)
            await self.add_execute_logs(uuid=uuid, app_uuid="", app_name="", result=result_text,
                                        status=1,
                                        html="<span>" + result_text + "</span>")
            raise

        if str(edge_action) == "1":
            is_arr = re.findall(r'\[\w*.+\]', edge_if_else)
            if len(is_arr) > 0:
                edge_if_else_arr = str(is_arr[0]).replace("[", "").replace("]", "").split(",")
                if if_else_result in edge_if_else_arr:
                    return True
                else:
                    return False
            else:
                is_json_arr = str(edge_if_else).split("==")

                if len(is_json_arr) == 2:
                    if str(is_json_arr[0]) == str(is_json_arr[1]):
                        return True
                    else:
                        return False
                else:
                    if str(edge_if_else) == str(if_else_result):
                        return True
                    else:
                        return False

        elif str(edge_action) == "2":
            is_arr = re.findall(r'\[\w*.+\]', edge_if_else)
            if len(is_arr) > 0:
                edge_if_else_arr = str(is_arr[0]).replace("[", "").replace("]", "").split(",")
                if if_else_result not in edge_if_else_arr:
                    return True
                else:
                    return False
            else:
                is_json_arr = str(edge_if_else).split("!=")

                if len(is_json_arr) == 2:
                    if str(is_json_arr[0]) != str(is_json_arr[1]):
                        return True
                    else:
                        return False
                else:
                    if str(edge_if_else) != str(if_else_result):
                        return True
                    else:
                        return False
        elif str(edge_action) == "3":
            is_arr = re.findall(r'{0}'.format(edge_if_else), if_else_result)
            if len(is_arr) > 0:
                return True
            else:
                return False
        elif str(edge_action) == "4":
            is_json_arr = re.findall(r'\{\w.*\}!=\w.*', edge_if_else)
            is_json_arr_equal = re.findall(r'\{\w.*\}==\w.*', edge_if_else)

            if len(is_json_arr) == 1:
                is_equal = False
                is_json_arr = is_json_arr[0].split("!=")
                json_key = str(is_json_arr[0])
                json_val = str(is_json_arr[1])
            else:
                is_equal = True
                is_json_arr = is_json_arr_equal[0].split("==")
                json_key = str(is_json_arr[0])
                json_val = str(is_json_arr[1])

            if len(is_json_arr) > 0:
                edge_if_else_key = json_key.replace("{", "").replace("}", "")
                edge_if_else_arr = edge_if_else_key.split("!>")

                is_json = self.is_json(json_text=if_else_result)

                if is_json is False:
                    result_text = "[参数错误] 非 JSON 格式变量"

                    await self.add_execute_logs(
                        uuid=uuid, app_uuid="", app_name="",
                        result=result_text,
                        status=1,
                        html="<span>" + result_text + "</span>")

                    raise

                try:
                    if_else_result = json.loads(json.loads(if_else_result))
                except:
                    if_else_result = json.loads(if_else_result)

                key_all = "if_else_result"
                key_front = "['"
                key_after = "']"
                key_number_front = "["
                key_number_after = "]"

                for k in edge_if_else_arr:
                    try:
                        int(k)
                        key_all += key_number_front + k + key_number_after
                    except ValueError:
                        k = str(k).replace("!!!", "")
                        key_all += key_front + k + key_after
                try:
                    if_else_result = eval(key_all)
                    if is_equal:
                        if str(if_else_result) == json_val:
                            return True
                        else:
                            return False
                    else:
                        if str(if_else_result) != json_val:
                            return True
                        else:
                            return False
                except IndexError:
                    result_text = "[解析错误] 未找到 JSON Index : {key}".format(key=edge_if_else_key)
                    await self.add_execute_logs(
                        uuid=uuid, app_uuid="", app_name="",
                        result=result_text,
                        status=1,
                        html="<span>" + result_text + "</span>"
                    )

                    raise

                except KeyError:
                    result_text = "[解析错误] 未找到 JSON KEY : {key}".format(key=edge_if_else_key)
                    await self.add_execute_logs(
                        uuid=uuid, app_uuid="", app_name="",
                        result=result_text,
                        status=1,
                        html="<span>" + result_text + "</span>"
                    )

                    raise

                except TypeError:
                    result_text = "[解析错误] JSON 格式不存在 : {key}".format(key=edge_if_else_key)
                    await self.add_execute_logs(
                        uuid=uuid, app_uuid="", app_name="",
                        result=result_text,
                        status=1,
                        html="<span>" + result_text + "</span>"
                    )

                    raise

    async def end_run(self, run_status, uuid):
        if run_status == 1:
            await self.decr_sum(uuid=uuid)
            # redis.delete(*redis.keys(pattern='*{key}*'.format(key=self.only_id)))
        else:
            await self.add_execute_logs(uuid=uuid, app_uuid=self.end_app, app_name="结束", result="剧本执行结束",
                                        status=0, html="<span>剧本执行结束</span>")
            await self.add_report()
            await self.decr_sum(uuid=uuid)
            # redis.delete(*redis.keys(pattern='*{key}*'.format(key=self.only_id)))

    async def decr_sum(self, uuid):
        if int(redis.decr("exec_sum")) < 0:
            redis.set("exec_sum", "0")

        if int(redis.decr(uuid + "&&exec_sum")) < 0:
            redis.set(uuid + "&&exec_sum", "0")

    async def run(self, uuid, controller_data=None, audit_status=None, audit_app=None, only_id=None,
                  user=None, start_app=None):
        redis.incr("exec_sum")
        redis.incr(uuid + "&&exec_sum")

        workflow_info = Workflow.select(
            'uuid',
            'name',
            'remarks',
            'start_app',
            'end_app',
            'input_app',
            'webhook_app',
            'timer_app',
            'for_list',
            'if_list',
            'audit_list',
            'flow_json',
            'flow_data',
            'controller_data',
            'local_var_data',
            'status'
        ).where(
            "uuid", uuid
        ).first()

        if workflow_info:
            if workflow_info.status == 1:
                return False

            run_status = 0

            try:
                self.workflow_name = workflow_info.name
                self.workflow_remarks = workflow_info.remarks
                self.start_app = workflow_info.start_app
                self.end_app = workflow_info.end_app
                self.input_app = workflow_info.input_app
                self.webhook_app = workflow_info.webhook_app
                self.timer_app = workflow_info.timer_app
                self.for_list = str(workflow_info.for_list).split(",")
                self.if_list = str(workflow_info.if_list).split(",")
                self.audit_list = str(workflow_info.audit_list).split(",")
                self.flow_json = json.loads(workflow_info.flow_json)
                self.flow_data = json.loads(workflow_info.flow_data)
                self.local_var_data = workflow_info.local_var_data
                self.controller_data = workflow_info.controller_data

                if controller_data != None:
                    self.controller_data = json.dumps(controller_data)

                self.node_link_data = await self.make_node_link(edges=self.flow_json["cells"])
                # self.node_name_list = await self.make_node_name(edges=self.flow_json["cells"])

                if audit_app:
                    self.only_id = only_id

                    if str(audit_status) == "2":
                        app_name = json.loads(self.controller_data)[audit_app]["node_name"]
                        await self.add_execute_logs(uuid=uuid, app_uuid=audit_app, app_name=app_name,
                                                    result="【{user}】拒绝了该剧本执行".format(user=user),
                                                    status=0, html="【{user}】拒绝了该剧本执行".format(user=user))

                    elif str(audit_status) == "1":
                        app_name = json.loads(self.controller_data)[audit_app]["node_name"]
                        await self.add_execute_logs(uuid=uuid, app_uuid=audit_app, app_name=app_name,
                                                    result="【{user}】通过了该剧本执行".format(user=user),
                                                    status=0, html="【{user}】通过了该剧本执行".format(user=user))

                        paths = await W5Tree().get_paths(d=self.node_link_data, start=start_app, end=self.end_app)
                        await self.make_var(self.local_var_data, self.controller_data)
                        run_status = await self.for_play_book(paths=paths, uuid=uuid)
                else:
                    await self.add_execute_logs(uuid=uuid, app_uuid=self.start_app, app_name="开始",
                                                result="剧本开始执行",
                                                status=0,
                                                html="<span>剧本开始执行</span>")

                    paths = await W5Tree().get_paths(d=self.node_link_data, start=self.start_app, end=self.end_app)
                    await self.make_var(self.local_var_data, self.controller_data)
                    run_status = await self.for_play_book(paths=paths, uuid=uuid)
            except Exception:
                logger.error("{work_name} {err}".format(work_name=self.workflow_name, err=traceback.format_exc()))
            finally:
                await self.end_run(run_status, uuid)


def auto_execute(uuid, s=None, controller_data=None, data=None, app_uuid=None, audit_status=None, audit_app=None,
                 only_id=None, user=None, start_app=None):
    if controller_data is None or data is None or app_uuid is None:
        pass
    else:
        controller_data = json.loads(controller_data)

        if Auto().is_json(data):
            controller_data[app_uuid] = {"text": json.dumps(data)}
        else:
            controller_data[app_uuid] = {"text": str(data)}

    loop = asyncio.get_event_loop()

    asyncio.run_coroutine_threadsafe(
        Auto(socket=s).run(
            uuid=uuid,
            controller_data=controller_data,
            audit_status=audit_status,
            audit_app=audit_app,
            only_id=only_id,
            user=user,
            start_app=start_app
        ), loop)

    # def run():
    #     asyncio.run(
    #         Auto(socket=s).run(
    #             uuid=uuid,
    #             controller_data=controller_data,
    #             audit_status=audit_status,
    #             audit_app=audit_app,
    #             only_id=only_id,
    #             user=user,
    #             start_app=start_app
    #         )
    #     )
    #
    # t = threading.Thread(target=run)
    # t.setDaemon(True)
    # t.start()
