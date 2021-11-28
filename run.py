#!/usr/bin/env python
# encoding:utf-8
import gevent.monkey

gevent.monkey.patch_all()

import sys
import platform


def w5_info(**kwargs):
    print(" ##@&$||;..!||||||||||;;||||||||%$@##@")
    print(" #@$%||||!`    .;|||||;. `:!||||||$@@@")
    print(" @$%||||||||!`               `!||||$@&")
    print(" &$||||||||||!.              :|||||%$$")
    print(" $%||||||||||`              `!||||||$$")
    print(" $%|||||||||;.                :|||||$$")
    print(" $%||||||||!.                  .;|||$$")
    print(" &$||||||||;      .!|:.          `!%$$")
    print(" @$%||||||||;. .:|||!'            .!&&")
    print(" #@$|||||||||||||||!`             '%@@")
    print(" ##@$%|||||||||||!`              :%@#@")
    print(" ###@&$||||||||!`               !&###@")
    print(" #####@&&%||||:.             `%&#####@")
    print(" ########&&&%:   W5 SOAR  '$&@#######@  v{version}".format(version="0.5.0"))
    print("=============================================")
    print("* Web : https://w5.io")
    print("* Github : https://github.com/w5hub/w5")
    print("=============================================")

    if platform.system() == 'Windows':
        print("* Running on http://{host}:{port}/ (Press CTRL+C to quit)".format(host=kwargs["host"],
                                                                                 port=kwargs["port"]))


def start_w5(**kwargs):
    w5_info(host=kwargs["host"], port=kwargs["port"])

    if platform.system() == 'Windows':
        from core import start
        from gevent import pywsgi
        from geventwebsocket.handler import WebSocketHandler

        server = pywsgi.WSGIServer((kwargs["host"], kwargs["port"]), start, handler_class=WebSocketHandler)
        server.serve_forever()
    else:
        import multiprocessing
        from gunicorn.app.wsgiapp import run as start_http

        workers = multiprocessing.cpu_count() * 2 + 1

        sys.argv.append("-k")
        sys.argv.append("flask_sockets.Worker")
        sys.argv.append("-b")
        sys.argv.append(kwargs["host"] + ":" + str(kwargs["port"]))
        sys.argv.append("-w")
        sys.argv.append(str(workers))
        sys.argv.append("-t")
        sys.argv.append("60")
        sys.argv.append("--threads")
        sys.argv.append("2")
        sys.argv.append("core:start")

        start_http()


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8888
    start_w5(host=host, port=port)
