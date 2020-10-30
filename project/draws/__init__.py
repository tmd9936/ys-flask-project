from flask import Blueprint
from flask import render_template, request, url_for
from flask import url_for, redirect, flash, session, abort

from flask_pymongo import ObjectId

from project import mongo

draw_blueprint = Blueprint(
                    'draw',
                    __name__,
                    template_folder='templates',
                    url_prefix='/draw')

from . import routes
