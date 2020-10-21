from flask import Blueprint

from flask import render_template, request, url_for
from flask import url_for, redirect, flash, session, abort, send_from_directory

from flask_pymongo import ObjectId

from project.commons import consts as const
from project.commons.decorates import login_required
from project.commons.common import *

from project import app

from project import mongo

import os

boards_blueprint = Blueprint(
            'board', 
            __name__, 
            template_folder='templates',
            url_prefix="/board")


from . import routes