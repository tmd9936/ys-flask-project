from flask import Blueprint
from flask import render_template, request, url_for
from flask import url_for, redirect, flash, session, abort

from flask_pymongo import ObjectId

from project import mongo

from project.commons.decorates import login_required

books_blueprint = Blueprint('book',
                            __name__,
                            template_folder='templates',
                            url_prefix="/book")

from . import routes
from . import crawl_yes24