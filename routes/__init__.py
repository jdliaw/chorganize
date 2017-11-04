from flask import Blueprint
routes = Blueprint('routes', __name__)

from .group import *
from .users import *