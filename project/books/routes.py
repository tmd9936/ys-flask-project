from . import *
from .crawl_yes24 import search_book, crwal_index
from datetime import datetime

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
    

@books_blueprint.route("/join/<book_num>", methods=["GET","POST"])
@login_required
def book_join(book_num):
    if book_num is not None and book_num != "":
        if request.method == "GET":
            result = crwal_index(book_num)

            if result is None:
                flash("존재하는 책이 아닙니다.")
                return redirect(url_for("book.book_search"))

            book_db = mongo.db.book

            current_utc_time = round(datetime.utcnow().timestamp()* 1000)

            book_data = {
                "member_id":session["id"],
                "name":result.get("name"),
                "publisher":result.get("auth"),
                "publishdate":result.get("date"),
                "perallstudy":0,
                "lastmodify":current_utc_time,
            }

            doc = book_db.insert_one(book_data)
            book_id = doc.inserted_id

            book_indexes_db = mongo.db.indexes

            indexes_data = list()
            for index in result.get("indexes"):
                indexes = dict()
                indexes["bookid"] = book_id
                indexes["memberid"] = session["id"]
                indexes["name"] = index
                indexes["perstudy"] = 0
                indexes["latestdate"] = current_utc_time
                
                indexes_data.append(indexes)

            book_indexes_db.insert_many(indexes_data)

      
            return render_template("book/join.html", title="책수정", result=result)
        else:
            pass
    else:
        flash("책 번호를 정확히 입력하세요.")
        redirect(url_for("book.book_search"))
    
    