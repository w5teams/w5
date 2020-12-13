import os
import json
import shutil
import asyncio
import requests
import platform
from core.model import *
from loguru import logger
from core import (db, redis)
from core.err import *
from core.utils.times import Time
from core.utils.randoms import Random
from core.utils.file import File
from flask import (request, current_app, Blueprint)

if platform.system() == 'Windows':
    from core.auto.windows.core import auto_execute
elif platform.system() == 'Linux':
    from core.auto.linux.core import auto_execute
elif platform.system() == "Darwin":
    from core.auto.mac.core import auto_execute
