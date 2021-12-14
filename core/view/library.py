import os
import json
import rpyc
import shutil
import asyncio
import requests
import platform
import threading
from core.model import *
from loguru import logger
from core import (db, redis)
from core.err import *
from core.utils.times import Time
from core.utils.randoms import Random
from core.utils.file import File
from core.utils.zip import Zip
from core.utils.pages import Page
from core.utils.version import Version as VersionUtil
from rpyc.utils.server import ThreadedServer
from flask import (request, current_app, Blueprint)
from werkzeug.utils import secure_filename

if platform.system() == 'Windows':
    from core.auto.windows.core import auto_execute, ManageTimer
elif platform.system() == 'Linux':
    from core.auto.linux.core import auto_execute, ManageTimer
elif platform.system() == "Darwin":
    print("Mac platform is not supported.")
