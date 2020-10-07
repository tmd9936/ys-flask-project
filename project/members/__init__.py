from flask import Blueprint
from flask import render_template, request, url_for
from flask import url_for, redirect, flash, session, abort

from flask_pymongo import ObjectId

from project import mongo

members_blueprint = Blueprint(
                    'member',
                    __name__,
                    template_folder='templates',
                    url_prefix='/member')

from . import routes