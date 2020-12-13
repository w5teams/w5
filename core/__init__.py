# !/usr/bin/env python
# encoding:utf-8
import os
import configparser
# from loguru import logger
from flask_cors import CORS
from flask_orator import Orator
from flask_redis import FlaskRedis
from flask_sockets import Sockets
from core.view import Decorator
from flask import (Flask, send_from_directory)

version = "0.1"

db = Orator()
redis = FlaskRedis()
sockets = Sockets()


# def init_log():
#     base = "/Users/sanjin/work/w5/x_w5/logs"
#
#     info_path = os.path.join(base, 'info.{time:YYYY-MM-DD}.log')
#     error_path = os.path.join(base, 'error.{time:YYYY-MM-DD}.log')
#
#     logger.remove()
#
#     logger_format = "{time:YYYY-MM-DD HH:mm:ss,SSS} [{thread}] {level} {file} {line} - {message}"
#
#     logger.add(info_path, format=logger_format, enqueue=True, rotation="00:00", retention='10 days',
#                encoding='utf-8', level='INFO')
#
#     logger.add(error_path, format=logger_format, enqueue=True, rotation="00:00", retention='10 days',
#                encoding='utf-8', level='ERROR')


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
    from core.view.workflow import ws as ws_workflow

    route_list = [r_login, r_user, r_type, r_variablen, r_system, r_apps, r_workflow, r_logs, r_dashboard, r_api]

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
    app.config['apps_path'] = app.config['project_path'] + "/apps"
    app.config['web_path'] = app.config['project_path'] + "/core/web"
    app.config['public_path'] = app.config['project_path'] + "/core/public"
    app.config['update_path'] = "http://w5-1253132429.cos.ap-beijing.myqcloud.com"

    cf = configparser.ConfigParser()
    cf.read(app.config['project_path'] + '/config.ini')

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
            r"/app/*": {"origins": "*"}
        }
    )


def init_decorator(app):
    no_path = [
        "/api/v1/w5/login",
        "/api/v1/w5/webhook"
    ]

    Decorator(app=app, no_path=no_path)


def init_web_sockets(app):
    sockets.init_app(app=app)


def init_w5(app):
    with open(app.config['apps_path'] + '/version.txt', 'r') as f:
        apps_version = f.read()
        from core.view.system.view import update_version, init_key
        update_version(w5_version=version, apps_version=apps_version)
        init_key()


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
