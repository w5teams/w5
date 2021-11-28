# !/usr/bin/env python
# encoding:utf-8
import os
import sys
import signal
import configparser
from flask_cors import CORS
from flask_orator import Orator
from flask_redis import FlaskRedis
from flask_sockets import Sockets
from core.view import Decorator
from flask import (Flask, send_from_directory)

version = "0.5.0"

db = Orator()
redis = FlaskRedis()
sockets = Sockets()

lose_time = None
max_instances = None
w5_apps_path = None


def init_route(app):
    from core.view.login import r as r_login
    from core.view.user import r as r_user
    from core.view.type import r as r_type
    from core.view.variablen import r as r_variablen
    from core.view.system import r as r_system
    from core.view.apps import r as r_apps
    from core.view.workflow import r as r_workflow
    from core.view.logs import r as r_logs
    from core.view.dashboard import r as r_dashboard
    from core.view.api import r as r_api
    from core.view.report import r as r_report
    from core.view.timer import r as r_timer
    from core.view.workflow import ws as ws_workflow

    route_list = [r_login, r_user, r_type, r_variablen, r_system, r_apps, r_workflow, r_logs, r_dashboard, r_api,
                  r_report, r_timer]

    for route in route_list:
        app.register_blueprint(route, url_prefix="/api/v1/w5")

    sockets.register_blueprint(ws_workflow, url_prefix=r'/')


def init_web(app):
    @app.route('/')
    def index():
        return app.send_static_file("index.html")

    @app.route('/<path:file>')
    def route(file):
        return app.send_static_file(file)


def init_apps(app):
    @app.route('/app/<path:file>')
    def app_icon(file):
        file_arr = str(file).split("/")

        file_name = file_arr[1]

        file_path = app.config['apps_path'] + "/" + file_arr[0]

        return send_from_directory(directory=file_path, filename=file_name)


def init_public(app):
    @app.route('/public/<path:file_name>')
    def public(file_name):
        return send_from_directory(directory=app.config['public_path'], filename=file_name)


def init_config(app):
    app.config['project_path'] = os.getcwd()
    app.config['tmp_path'] = app.config['project_path'] + "/tmp"
    app.config['apps_path'] = app.config['project_path'] + "/apps"
    app.config['web_path'] = app.config['project_path'] + "/core/web"
    app.config['public_path'] = app.config['project_path'] + "/core/public"
    app.config['update_path'] = "https://s.w5soar.com"

    cf = configparser.RawConfigParser()
    cf.read(app.config['project_path'] + '/config.ini')

    global lose_time, max_instances, w5_apps_path
    lose_time = cf.get("setting", "lose_time")
    max_instances = cf.get("setting", "max_instances")
    w5_apps_path = app.config['apps_path']

    if os.getenv('MYSQL_HOST'):
        app.config['ORATOR_DATABASES'] = {
            'development': {
                'driver': 'mysql',
                'host': os.getenv('MYSQL_HOST'),
                'port': int(os.getenv('MYSQL_PORT')),
                'database': os.getenv('MYSQL_DATABASE'),
                'user': os.getenv('MYSQL_USER'),
                'password': os.getenv('MYSQL_PASSWORD')
            }
        }
    else:
        app.config['ORATOR_DATABASES'] = {
            'development': {
                'driver': 'mysql',
                'host': cf.get("mysql", "host"),
                'port': int(cf.get("mysql", "port")),
                'database': cf.get("mysql", "database"),
                'user': cf.get("mysql", "user"),
                'password': cf.get("mysql", "password")
            }
        }

    if os.getenv('REDIS_HOST'):
        redis_host = os.getenv('REDIS_HOST')
        redis_port = os.getenv('REDIS_PORT')
        redis_database = os.getenv('REDIS_DATABASE')
        redis_password = os.getenv('REDIS_PASSWORD')
    else:
        redis_host = cf.get("redis", "host")
        redis_port = cf.get("redis", "port")
        redis_database = cf.get("redis", "database")
        redis_password = cf.get("redis", "password")

    if str(redis_password) == "":
        app.config['REDIS_URL'] = "redis://{host}:{port}/{db}".format(
            host=redis_host,
            port=redis_port,
            db=redis_database
        )
    else:
        app.config['REDIS_URL'] = "redis://:{password}@{host}:{port}/{db}".format(
            password=redis_password,
            host=redis_host,
            port=redis_port,
            db=redis_database
        )


def init_db(app):
    db.init_app(app=app)
    redis.init_app(app=app)


def init_cors(app):
    CORS(
        app=app,
        resources={
            r"/api/*": {"origins": "*"},
            r"/app/*": {"origins": "*"},
            r"/public/*": {"origins": "*"}
        }
    )


def init_decorator(app):
    no_path = [
        "/api/v1/w5/login",
        "/api/v1/w5/webhook",
        "/api/v1/w5/get/workflow_exec",
        "/api/v1/w5/get/workflow_success_fail",
        "/api/v1/w5/get/workflow_logs",
        "/api/v1/w5/get/executing"
    ]

    Decorator(app=app, no_path=no_path)


def init_web_sockets(app):
    sockets.init_app(app=app)


def init_w5(app):
    from core.view.system.view import init_key, init_timer
    init_key()
    init_timer()


def init_app():
    app = Flask(__name__, static_folder="web")

    init_config(app=app)
    init_cors(app=app)
    init_db(app=app)
    init_web(app=app)
    init_public(app=app)
    init_apps(app=app)
    init_route(app=app)
    init_decorator(app=app)
    init_web_sockets(app=app)
    init_w5(app=app)

    app.app_context().push()

    return app


start = init_app()


def sign_out(signum, frame):
    try:
        redis.delete("manage_timer_lock")
    except:
        pass

    sys.exit()


signal.signal(signal.SIGINT, sign_out)
