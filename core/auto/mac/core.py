#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
import re
import copy
import json
import asyncio
import platform
import threading
import importlib
from loguru import logger
from core import redis
from rpyc import Service
from core.utils.times import Time
from core.utils.file import File
from core.utils.randoms import Random
from core import (lose_time, max_instances, w5_apps_path)
from core.model import Logs, Workflow, Variablen, Report, Timer
from apscheduler.schedulers.gevent import GeventScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.base import JobLookupError


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
            w5_timer.update_date(self.timer_app, self.config["time"])
        elif self.config["type"] == "interval":
            w5_timer.update_interval(self.timer_app, self.config["interval_type"], int(self.config["time"]),
                                     start_date=self.config["start_date_x"],
                                     end_date=self.config["end_date_x"],
                                     jitter=self.config["jitter"])
        elif self.config["type"] == "cron":
            w5_timer.update_cron(self.timer_app, self.config["time"], start_date=self.config["start_date_x"],
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


class Auto(object):
    def __init__(self, socket=None):
        self.workflow_name = None
        self.workflow_remarks = None
        self.socket = socket
        self.only_id = Random.make_order_number(length=10)
        self.flow_json = None
        self.flow_data = None
        self.local_var_data = None
        self.global_var_data = None
        self.start_app = None
        self.end_app = None
        self.input_app = None
        self.webhook_app = None
        self.timer_app = None

    def is_json(self, json_text):
        try:
            int(json_text)
            return False
        except Exception:
            try:
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
            if self.timer_app == "" or self.timer_app is None:
                controller_var = json.loads(controller_var)

                for x in controller_var:
                    key = x + "&&" + self.only_id + "&&text"
                    redis.set(key, controller_var[x]["text"], ex=lose_time)

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
            self.socket.send(json.dumps(data))

    async def add_report(self):
        report_info = {
            'report_no': self.only_id,
            'workflow_name': self.workflow_name,
            'remarks': self.workflow_remarks,
            'create_time': Time.get_date_time()
        }

        Report.insert(report_info)

    async def execute(self, app_uuid, app_dir=None, data=None):

        args_data = copy.deepcopy(data)

        if app_dir:
            args_data["app_dir"] = app_dir

        args_data_json_x = json.dumps(args_data)

        if self.input_app == app_uuid or self.webhook_app == app_uuid:
            key = app_uuid + "&&" + self.only_id + "&&text"
            return {"status": 0, "result": redis.get(key).decode(), "args": args_data_json_x, "html": ""}

        if self.timer_app == app_uuid:
            return {"status": 0, "result": "定时器正在执行", "args": args_data_json_x, "html": ""}

        is_identification = await self.is_identification(app_dir=app_dir)

        if is_identification == False:
            return {"status": 1, "result": "请勿使用非法应用", "args": args_data_json_x, "html": ""}

        is_public_status, is_public = await self.is_public(app_dir=app_dir)

        if is_public_status == 0:
            return {"status": 1, "result": "请配置 is_public", "args": args_data_json_x, "html": ""}

        import_path = ""

        if platform.system() == 'Windows':
            import_path = 'apps.' + str(app_dir) + '.windows.run'
        elif platform.system() == 'Linux':
            import_path = 'apps.' + str(app_dir) + '.linux.run'
        elif platform.system() == "Darwin":
            import_path = 'apps.' + str(app_dir) + '.mac.run'

        try:
            data["app"] = importlib.import_module(import_path)
            app_action = getattr(data["app"], data["action"])
        except Exception as e:
            return {"status": 1, "result": "请使用正确的应用", "args": args_data_json_x, "html": ""}

        args = ""

        for key in data:
            if key != "node_name" and key != "action" and key != "app" and key != "action_name" and key != "description" and key != "app_dir":
                args = args + "," + key

                var_status, text = await self.analysis_var(text=str(data[key]))

                redis_key = app_uuid + "&&" + self.only_id + "&&" + key
                redis.set(redis_key, text, ex=lose_time)

                if var_status == 0:
                    data[key] = text
                    args_data[key] = text
                else:
                    return {"status": var_status, "result": text, "args": args_data_json_x, "html": ""}

        args_data_json = json.dumps(args_data)

        try:
            kwargs = {}
            for arg in args[1:].split(","):
                if arg in data:
                    kwargs[arg] = data[arg]
            result_data = await app_action(**kwargs)
        except TypeError as e:
            return {"status": 1, "result": "请勿使用非法应用", "args": args_data_json, "html": ""}

        if "status" not in result_data:
            return {"status": 2, "result": "APP 错误，请检测 status 返回字段", "args": args_data_json, "html": ""}

        if "result" not in result_data:
            return {"status": 2, "result": "APP 错误，请检测 result 返回字段", "args": args_data_json, "html": ""}

        if "html" not in result_data:
            html_data = ""
        else:
            html_data = result_data["html"]

        return {"status": result_data["status"], "result": result_data["result"], "args": args_data_json,
                "html": html_data}

    async def get_app_data(self, uuid, app_uuid, app_info=None):
        key_result = app_uuid + "&&" + self.only_id + "&&result"
        key_status = app_uuid + "&&" + self.only_id + "&&status"

        if self.input_app == app_uuid or self.webhook_app == app_uuid or self.timer_app == app_uuid:
            if redis.exists(key_result) == 0:
                result_data = await self.execute(app_uuid=app_uuid)

                is_json = self.is_json(json_text=result_data["result"])

                if is_json:
                    result = json.dumps(result_data["result"])
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
            if redis.exists(key_result) == 0:
                result_data = await self.execute(app_uuid=app_uuid, app_dir=app_info["app_dir"],
                                                 data=app_info["data"])

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

    async def find_start_app(self, edges, start_app=None):
        for r in edges:
            if start_app:
                if str(r["source"]) == start_app:
                    return r["target"]

    async def find_next_app(self, edges, next_app=None):
        num = 0

        for r in edges:
            if next_app:
                edge_info_action = ""
                edge_info_if_else = ""
                edge_info_switch = False

                if r["id"] in self.flow_data:
                    edge_info = self.flow_data[r["id"]]
                    edge_info_action = edge_info["action"]
                    edge_info_if_else = edge_info["ifelse"]
                    edge_info_switch = edge_info["switch"]

                key = next_app + "&&" + self.only_id + "&&sum"
                if redis.exists(key) == 1:
                    sum = redis.get(key)

                    if str(r["source"]) == next_app:
                        if num != int(sum):
                            num = num + 1
                        else:
                            return str(r["label"]), r["source"], r[
                                "target"], edge_info_switch, str(edge_info_action), str(edge_info_if_else)
                else:
                    if str(r["source"]) == next_app:
                        return str(r["label"]), r["source"], r[
                            "target"], edge_info_switch, str(edge_info_action), str(edge_info_if_else)

    async def decr_sum(self, uuid):
        if int(redis.decr("exec_sum")) < 0:
            redis.set("exec_sum", "0")

        if int(redis.decr(uuid + "&&exec_sum")) < 0:
            redis.set(uuid + "&&exec_sum", "0")

    async def run(self, uuid):
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
            'flow_json',
            'flow_data',
            'controller_data',
            'local_var_data',
            'status'
        ).where(
            "uuid", uuid
        ).first()

        if workflow_info:
            if str(workflow_info.status) == "1":
                return False

            self.workflow_name = workflow_info.name
            self.workflow_remarks = workflow_info.remarks
            self.start_app = workflow_info.start_app
            self.end_app = workflow_info.end_app
            self.input_app = workflow_info.input_app
            self.webhook_app = workflow_info.webhook_app
            self.timer_app = workflow_info.timer_app
            self.flow_json = json.loads(workflow_info.flow_json)
            self.flow_data = json.loads(workflow_info.flow_data)

            await self.make_var(workflow_info.local_var_data, workflow_info.controller_data)

            target_app = await self.find_start_app(edges=self.flow_json["edges"], start_app=self.start_app)

            await self.add_execute_logs(uuid=uuid, app_uuid=self.start_app, app_name="开始", result="剧本开始执行", status=0,
                                        html="<span>剧本开始执行</span>")
            is_while = True

            while is_while:
                try:
                    edge_name, source_app, next_app, is_switch, edge_action, edge_if_else = await self.find_next_app(
                        edges=self.flow_json["edges"],
                        next_app=target_app
                    )
                    if edge_if_else:
                        final_res = ''
                        for temp_str in edge_if_else.split(','):
                            if temp_str.startswith('@'):
                                temp_status, temp_item = await self.analysis_var(edge_if_else)
                                final_res = final_res + temp_item + ','
                            else:
                                final_res = final_res + temp_str + ','
                        if final_res:
                            edge_if_else = final_res[:-1]
                        else:
                            edge_if_else = final_res
                except Exception as e:
                    await self.add_execute_logs(uuid=uuid, app_uuid="", app_name="", result="当前剧本不具有可执行条件", status=1,
                                                html="<span>当前剧本不具有可执行条件</span>")

                    await self.add_execute_logs(uuid=uuid, app_uuid=self.end_app, app_name="结束",
                                                result="剧本执行结束",
                                                status=0, html="<span>剧本执行结束</span>")

                    await self.decr_sum(uuid=uuid)
                    is_while = False
                    break

                key = target_app + "&&" + self.only_id + "&&sum"
                if redis.exists(key) == 1:
                    sum = redis.get(key)
                    redis.set(key, int(sum) + 1, ex=lose_time)
                else:
                    redis.set(key, 1, ex=lose_time)

                if self.input_app == source_app or self.webhook_app == source_app or self.timer_app == source_app:
                    is_status, if_else_result = await self.get_app_data(uuid=uuid, app_uuid=source_app)
                else:
                    source_info = self.flow_data[source_app]
                    is_status, if_else_result = await self.get_app_data(uuid=uuid, app_uuid=source_app,
                                                                        app_info=source_info)

                if str(is_status) == "0":
                    if is_switch:
                        if str(edge_action) == "1":
                            is_arr = re.findall(r'\[\w*.+\]', edge_if_else)
                            if len(is_arr) > 0:
                                edge_if_else_arr = str(is_arr[0]).replace("[", "").replace("]", "").split(",")
                                if if_else_result in edge_if_else_arr:
                                    target_app = next_app
                                else:
                                    pass
                            else:
                                if str(edge_if_else) == str(if_else_result):
                                    target_app = next_app
                                else:
                                    pass
                        elif str(edge_action) == "2":
                            is_arr = re.findall(r'\[\w*.+\]', edge_if_else)
                            if len(is_arr) > 0:
                                edge_if_else_arr = str(is_arr[0]).replace("[", "").replace("]", "").split(",")
                                if if_else_result not in edge_if_else_arr:
                                    target_app = next_app
                                else:
                                    pass
                            else:
                                if str(edge_if_else) != str(if_else_result):
                                    target_app = next_app
                                else:
                                    pass
                        elif str(edge_action) == "3":
                            is_arr = re.findall(r'{0}'.format(edge_if_else), if_else_result)
                            if len(is_arr) > 0:
                                target_app = next_app
                            else:
                                pass
                        elif str(edge_action) == "4":
                            is_json_arr = re.findall(r'\{\w.*\}!=\w.*', edge_if_else)
                            is_json_arr_equal = re.findall(r'\{\w.*\}=\w.*', edge_if_else)

                            if len(is_json_arr) == 1:
                                is_equal = False
                                is_json_arr = is_json_arr[0].split("!=")
                                json_key = str(is_json_arr[0])
                                json_val = str(is_json_arr[1])
                            else:
                                is_equal = True
                                is_json_arr = is_json_arr_equal[0].split("=")
                                json_key = str(is_json_arr[0])
                                json_val = str(is_json_arr[1])

                            if len(is_json_arr) > 0:
                                edge_if_else_key = json_key.replace("{", "").replace("}", "")
                                edge_if_else_arr = edge_if_else_key.split("!>")

                                is_json = self.is_json(json_text=if_else_result)

                                if is_json is False:
                                    await self.add_execute_logs(
                                        uuid=uuid, app_uuid="", app_name="",
                                        result="非 JSON 格式变量",
                                        status=1,
                                        html="<span>非 JSON 格式变量</span>")

                                    await self.add_execute_logs(uuid=uuid, app_uuid=self.end_app, app_name="结束",
                                                                result="剧本执行结束",
                                                                status=0, html="<span>剧本执行结束</span>")

                                    await self.decr_sum(uuid=uuid)
                                    is_while = False
                                    break

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
                                            target_app = next_app
                                        else:
                                            pass
                                    else:
                                        if str(if_else_result) != json_val:
                                            target_app = next_app
                                        else:
                                            pass
                                except IndexError:
                                    await self.add_execute_logs(
                                        uuid=uuid, app_uuid="", app_name="",
                                        result="未找到 JSON Index : {key}".format(key=edge_if_else_key),
                                        status=1,
                                        html="<span>未找到 JSON Index : {key}</span>".format(key=edge_if_else_key))

                                    await self.add_execute_logs(uuid=uuid, app_uuid=self.end_app, app_name="结束",
                                                                result="剧本执行结束",
                                                                status=0, html="<span>剧本执行结束</span>")

                                    await self.decr_sum(uuid=uuid)
                                    is_while = False
                                    break
                                except KeyError:
                                    await self.add_execute_logs(
                                        uuid=uuid, app_uuid="", app_name="",
                                        result="未找到 JSON KEY : {key}".format(key=edge_if_else_key),
                                        status=1,
                                        html="<span>未找到 JSON KEY : {key}</span>".format(key=edge_if_else_key))

                                    await self.add_execute_logs(uuid=uuid, app_uuid=self.end_app, app_name="结束",
                                                                result="剧本执行结束",
                                                                status=0, html="<span>剧本执行结束</span>")

                                    await self.decr_sum(uuid=uuid)
                                    is_while = False
                                    break
                                except TypeError:
                                    await self.add_execute_logs(
                                        uuid=uuid, app_uuid="", app_name="",
                                        result="JSON 格式不存在 : {key}".format(key=edge_if_else_key),
                                        status=1,
                                        html="<span>JSON 格式不存在 : {key}</span>".format(key=edge_if_else_key))

                                    await self.add_execute_logs(uuid=uuid, app_uuid=self.end_app, app_name="结束",
                                                                result="剧本执行结束",
                                                                status=0, html="<span>剧本执行结束</span>")

                                    await self.decr_sum(uuid=uuid)
                                    is_while = False
                                    break
                    else:
                        target_app = next_app
                else:
                    await self.add_execute_logs(uuid=uuid, app_uuid=self.end_app, app_name="结束", result="剧本执行结束",
                                                status=0, html="<span>剧本执行结束</span>")
                    await self.decr_sum(uuid=uuid)
                    is_while = False
                    break

                if next_app == self.end_app:
                    await self.add_execute_logs(uuid=uuid, app_uuid=self.end_app, app_name="结束", result="剧本执行结束",
                                                status=0, html="<span>剧本执行结束</span>")
                    await self.add_report()
                    await self.decr_sum(uuid=uuid)
                    # redis.delete(*redis.keys(pattern='*{key}*'.format(key=self.only_id)))
                    is_while = False
                    break


def auto_execute(uuid, s=None, controller_data=None, text=None, app_uuid=None):
    if controller_data is None or text is None or app_uuid is None:
        pass
    else:
        controller_data = json.loads(controller_data)

        if Auto().is_json(text):
            controller_data[app_uuid] = {"text": json.dumps(text)}
        else:
            controller_data[app_uuid] = {"text": str(text)}

        Workflow.where('uuid', uuid).update({
            'controller_data': json.dumps(controller_data),
            'update_time': Time.get_date_time()
        })

    def thread_exec():
        async def run():
            await asyncio.gather(Auto(socket=s).run(uuid=uuid))

        try:
            asyncio.run(run())
        except RuntimeError:
            asyncio.gather(Auto(socket=s).run(uuid=uuid))

    t = threading.Thread(target=thread_exec)
    t.setDaemon(True)
    t.start()
