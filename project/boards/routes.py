from . import *
import math
from datetime import datetime
from flask import Response

@boards_blueprint.route("/upload_image", methods=["POST"])
def upload_image():
    if request.method == "POST":
        file = request.files["image"]
        if file and allowed_file(file.filename):
            filename = "{}.jpg".format(rand_generator())
            
            savefilepath = os.path.join(app.config["BOARD_IMAGE_PATH"], filename)
            file.save(savefilepath)
            return url_for("board.board_images", filename = filename)

@boards_blueprint.route("/images/<filename>")
def board_images(filename):
    return send_from_directory(app.config["BOARD_IMAGE_PATH"], filename)

@boards_blueprint.route("/files/<filename>")
def board_files(filename):
    return send_from_directory(app.config["BOARD_ATTACH_FILE_PATH"], filename, as_attachment=True)

def board_delete_attach_file(filename):
    abs_path = os.path.join(app.config["BOARD_ATTACH_FILE_PATH"],filename)
    if os.path.exists(abs_path):
        os.remove(abs_path)
        return True
    return False

@boards_blueprint.route('/list')
def list():
    page = request.args.get("page", default=1, type=int)
    app.config["BOARD_IMAGE_PATH"]
    limit = request.args.get("limit", const.PAGE_LIMIT, type=int)

    search = request.args.get("search", -1, type=int)

    keyword = request.args.get("keyword", "", type=str)

    query = {}

    search_list = []

    if search == 0:
        search_list.append({"title":{"$regex" : keyword}})
    elif search == 1:
        search_list.append({"contents":{"$regex" : keyword}})
    elif search == 2:
        search_list.append({"title":{"$regex" : keyword}})
        search_list.append({"contents":{"$regex" : keyword}})
    elif search == 3:
        search_list.append({"name":{"$regex" : keyword}})

    if len(search_list) > 0:
        query = {"$or":search_list}

    board = mongo.db.board
    docs = board.find(query).skip((page-1)*limit).limit(limit).sort("regdate",-1)

    tot_count = board.find(query).count()

    last_page_num = math.ceil(tot_count / limit)

    block_size = 5

    block_num = int((page-1)/ block_size)
    
    block_start = int((block_size*block_num) + 1)

    block_last = block_start+(block_size - 1)

    if block_last > last_page_num:
        block_last = last_page_num

    return render_template("bbs/list.html", docs = docs, 
                                        limit = limit,
                                        page = page,
                                        block_start = block_start,
                                        block_last = block_last,
                                        last_page_num = last_page_num,
                                        keyword=keyword,
                                        search=search,
                                        title='리스트')    



@boards_blueprint.route("/view/<idx>")
@login_required
def board_view(idx):
    page = request.args.get("page", default=1, type=int)
    search = request.args.get("search",-1,type=int)
    keyword = request.args.get("keyword",'',str)

    if idx is not None:
        board = mongo.db.board
        data = board.find_one_and_update(
            {"_id":ObjectId(idx)},
            {"$inc":{"hit":1}}, return_document=True)


        if data is not None:
            _id = data.get("_id")
            result = {
                "id" : _id,
                "name" : data.get("name"),
                "title" : data.get("title"),
                "contents" : data.get("contents"),
                "regdate" :data.get("regdate"),
                "hit" : data.get("hit"),
                "writer_id" : data.get("writer_id"),
                "attachFile":data.get("attachFile")
            }

            print(result.get("attachFile"))

            next_board = board.find_one({"_id":{"$gt":_id}})

            prev_board = board.find_one({"_id":{"$lt":_id}})

            if next_board is None:
                next_board_id = None
            else:
                next_board_id = next_board.get('_id')
            
            if prev_board is None:
                prev_board_id = None
            else:
                prev_board_id = prev_board.get('_id')
            

            return render_template("bbs/view.html", result = result, 
                                                search = search, 
                                                keyword = keyword, 
                                                page=page, 
                                                next_board_id=next_board_id, 
                                                prev_board_id=prev_board_id,
                                                title=data.get("title"))

    return abort(404)

@boards_blueprint.route("/write", methods=["GET", "POST"])
@login_required
def board_write():
    if request.method == "POST":
        filename = None
        if "attachFile" in request.files:
            file = request.files["attachFile"]
            if file and allowed_file(file.filename):
                filename = check_filename(file.filename)
                file.save(os.path.join(app.config["BOARD_ATTACH_FILE_PATH"], filename))
        


        name = request.form.get("name")
        title = request.form.get("title")
        contents = request.form.get("contents")


        # print(name, title, contents)

        # UTC는 국제 표준시 (참고: GMT(Greenwich Mean Time) - 그리니치 평균시, 세계 협정시)
        # UTC와 GMT는 혼용되어 사용됨, 시간차가 거의 없음.


        # UTC Time은 밀리세컨드(millisecond: 1000분의 1초)로 표현되기 때문 *1000을 해주고
        # 소수점이 나오는 걸 방지하기 위해 round함수로 반올림 해준다.
        current_utc_time = round((datetime.utcnow().timestamp()) * 1000)


        # board 컬렉션 생성해서 board라는 이름으로 받음
        board = mongo.db.board

        post_data = {
            "name":name,
            "title":title,
            "contents":contents,
            "regdate": current_utc_time,
            # 글 수정 삭제시 본인의 글인지 확인하기 위한 용도
            "writer_id":session.get("id"), 
            "hit" : 0
        }

        if filename is not None:
            post_data["attachFile"] = filename
            print("filename : " + filename)


        doc = board.insert_one(post_data)
        # print(doc.inserted_id)
        # print(contents)


        # 렌더링을 할 경우에는 inserted_id는 Object객체이므로 문자열로 형변환 해야한다
        # return str(doc.inserted_id)
        return redirect(url_for("board.board_view", idx=doc.inserted_id))
    else :
        return render_template("bbs/write.html", title="글쓰기") 


@boards_blueprint.route("/modify/<idx>", methods=["GET", "POST"])
@login_required
def board_modify(idx):
    if request.method == "GET":
        board = mongo.db.board
        data = board.find_one({"_id":ObjectId(idx)})

        if data is None:
            flash('게시물이 없습니다.')
            return redirect(url_for("board.list"))
        else:
            if session.get("id") == data.get("writer_id"):
                return render_template("bbs/modify.html", data=data, title="글수정")
            else:
                flash('글 수정 권한이 없습니다.')
                return redirect(url_for("board.board_view", idx=idx))
    
    else:
        title = request.form.get('title')
        contents = request.form.get('contents')
        delOldFile = request.form.get("delOldFile", "")

        board = mongo.db.board
        data = board.find_one({"_id":ObjectId(idx)})


        if session.get('id') == data.get('writer_id'):
            filename = None
            if "attachFile" in request.files: # 새로운 첨부파일이 있으면
                file = request.files["attachFile"] 
                if file and allowed_file(file.filename): # 파일형식이 있는지 확인
                    filename = check_filename(file.filename)
                    file.save(os.path.join(app.config["BOARD_ATTACH_FILE_PATH"], filename))

                    if data.get("attachFile"):
                        board_delete_attach_file(data.get("attachFile"))
            else: # 새로운 첨부파일이 없는 경우
                if delOldFile == "on":
                    filename = None
                    if data.get("attachFile"):
                        board_delete_attach_file(data.get("attachFile"))
                    else:
                        filename = data.get("attachFile")

            board.update_one({"_id":ObjectId(idx)},
                {"$set":
                    {
                        "title":title,
                        "contents":contents,
                        "attachFile":filename
                    }
                }
            )

            flash('수정되었습니다.')
            return redirect(url_for("board.board_view", idx=idx))
        else:
            flash("글 수정 권한이 없습니다.")
            return redirect(url_for("board.list"))


@boards_blueprint.route("/delete/<idx>")
def board_delete(idx):
    board = mongo.db.board
    data = board.find_one({"_id":ObjectId(idx)})

    if data.get("writer_id") == session.get("id"):
        board.delete_one({"_id":ObjectId(idx)})
        flash("삭제완료")
    else:
        flash("대상이 없습니다.")
    
    return redirect(url_for('board.list'))
