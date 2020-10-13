from . import *
from .crawl_yes24 import search_book, crwal_index
from datetime import datetime

@books_blueprint.route("/list", methods=["GET"])
@login_required
def book_list():
    book_db = mongo.db.book
    books = book_db.find({"member_id":session["id"]})

    return render_template("book/list.html", title="책장", books=books)

@books_blueprint.route("/view/<book_id>", methods=["GET"])
@login_required
def book_view(book_id):
    book_db = mongo.db.book
    book_info = book_db.find_one({"_id":ObjectId(book_id)})

    print(book_info)

    return render_template("book/view.html", title="책", book_info=book_info)

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

            # is_chk = book_db.find_one({"member_id":session["id"], "book_num":book_num})

            # if is_chk is not None:
            #     flash("이미 등록되어있는 책입니다.")
            #     return redirect(url_for("book.book_search"))


            current_utc_time = round(datetime.utcnow().timestamp()* 1000)

            book_data = {
                "member_id":session["id"],
                "book_num":book_num,
                "name":result.get("name"),
                "publisher":result.get("publisher"),
                "publish_date":result.get("date"),
                "per_all_study":0,
                "auth":result.get("auth"),
                "last_modify":current_utc_time,
                "image":result.get("image")
            }

            doc = book_db.insert_one(book_data)
            book_id = doc.inserted_id

            book_indexes_db = mongo.db.indexes

            indexes_data = list()
            for e_idx, index in enumerate(result.get("indexes")):
                indexes = dict()
                indexes["book_id"] = book_id
                indexes["member_id"] = session["id"]
                indexes["name"] = index
                indexes["per_study"] = 0
                indexes["depth"] = 0
                indexes["num"] = e_idx
                indexes["latest_date"] = current_utc_time
                
                indexes_data.append(indexes)

            book_indexes_db.insert_many(indexes_data)

            return redirect(url_for('book.book_modify',title="수정", member_id=session["id"], book_num=book_num))

    else:
        flash("책 번호를 정확히 입력하세요.")
        redirect(url_for("book.book_search"))
    
    
@books_blueprint.route("/modify/<member_id>/<book_num>", methods=["GET","POST"])
@login_required
def book_modify(member_id, book_num):
    if session["id"] != member_id:
        flash("확인 할 수 없습니다..")
        return redirect(url_for("book.book_search"))
    else:
        if request.method == "GET":
            book_db = mongo.db.book
            indexes_db = mongo.db.indexes

            # print(member_id, book_num)

            book_info = book_db.find_one({"member_id":member_id, "book_num":book_num})
            book_id = book_info.get("_id")

            book_indexes = indexes_db.find({"member_id":member_id, "book_id":book_id}).sort("num")

            return render_template("book/modify.html",title=book_info.get("name"), book_info=book_info, book_indexes= book_indexes)
        else:
            indexes_db = mongo.db.indexes
            
            book_id = request.form.get('book_id')
            depthes = request.form.getlist('depth')
            index_ids = request.form.getlist('index_id')
            indexes = request.form.getlist('book_index')

            for e_idx in range(0, len(indexes)):
                
                if index_ids[e_idx] == "" or index_ids[e_idx] is None:
                    current_utc_time = round(datetime.utcnow().timestamp()* 1000)
                    
                    indexes = dict()
                    indexes["book_id"] = book_id
                    indexes["member_id"] = member_id
                    indexes["name"] = indexes[e_idx]
                    indexes["per_study"] = 0
                    indexes["depth"] = depthes[e_idx]
                    indexes["num"] = e_idx
                    indexes["latest_date"] = current_utc_time

                    indexes_db.insert_one(indexes)
                else:
                    indexes_db.update({"_id":ObjectId(index_ids[e_idx])},
                    {"$set": 
                        {
                            "depth":depthes[e_idx],
                            "num":e_idx,
                            "name":indexes[e_idx]
                        }
                    })


            # print(depthes)
            # print(index_ides)
            # print(indexes)

            return redirect(url_for('book.book_view', book_id=book_id))

@books_blueprint.route("/delete/index/<index_id>", methods=["POST"])
@login_required
def delete_index(index_id):
    if index_id != "" and index_id is not None:
        indexes_db = mongo.db.indexes
        result = indexes_db.delete_one({"_id":ObjectId(index_id)})
        
        resp = jsonify(success=True)
        resp.status_code = 200
        
        return resp
    else:
        return jsonify({'error': 'This is not index id'}), 401