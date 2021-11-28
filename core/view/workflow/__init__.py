from core.view.library import *

r = Blueprint('workflow', __name__)
ws = Blueprint(r'ws', __name__)

from . import view
