from . import *
from .crawl_yes24 import search_book

@books_blueprint.route("/list", methods=["GET"])
@login_required
def book_list():
    return render_template("book/list.html", title="책장")

@books_blueprint.route("/search", methods=["GET"])
@login_required
def book_search():
    return render_template("book/search.html", title="검색")
    

@books_blueprint.route("/search/result/<search_str>/<page>", methods=["POST"])
@login_required
def book_search_result(search_str, page):
    lis = search_book(search_str, page)

    return lis
    