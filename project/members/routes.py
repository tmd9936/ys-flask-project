from . import *
from datetime import datetime


@members_blueprint.route("/join", methods=["GET", "POST"])
def member_join():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        pw = request.form.get('pw')
        pw2 = request.form.get('pw2')

        if name == "" or email == "" or pw == "" or pw2 == "":
            flash("값이 입력되지 않았습니다. 다시 확인하세요")
            return render_template("member/join.html", title="회원가입")
        
        if pw != pw2:
            flash("비밀번호가 다릅니다!")
            return render_template("member/join.html", title="회원가입")
        
        # 멤버객체 생성
        members = mongo.db.members

        # 중복 검사
        cnt = members.find({"email":email}).count()

        if cnt > 0:
            flash("중복된 이메일입니다.")
            return render_template("memeber/join.html", title="회원가입")
        
        current_utc_time = round(datetime.utcnow().timestamp()* 1000)

        post_data = {
            "name":name,
            "email":email,
            "pw":pw,
            "login_time": current_utc_time,
            "login_count":0
        }

        members.insert_one(post_data)

        return redirect(url_for('home'))
    else:
        return render_template("member/join.html", title="회원가입")
    

@members_blueprint.route("/login", methods=["GET","POST"])
def member_login():
    if request.method == "POST":
        email = request.form.get("email")
        pw = request.form.get("pw")

        next_url = request.form.get("next_url")

        members = mongo.db.members
        doc = members.find_one({"email":email})

        if doc is None:
            flash("이메일이 존재하지 않습니다.")
            return render_template("member/login.html", title="로그인")
        else:
            if doc.get("pw") == pw:
                session["email"] = email
                session["name"] = doc.get("name")
                session["id"] = str(doc.get("_id"))

                # 세션의 유지시간을 조작가능 설정
                session.permanet = True

                if next_url is not None:
                    return redirect(next_url)
                else:
                    return redirect(url_for('book.book_list'))
            else:
                flash("비밀번호가 틀립니다.")
                return render_template("member/login.html", title="로그인")


    else:
        return render_template("member/login.html", title="로그인")


@members_blueprint.route("/modify", methods=["GET","POST"])
def member_modify():
    if request.method == "POST":
        name = request.form.get('name')
        pw = request.form.get('pw')
        pw2 = request.form.get('pw2')

        if name == "" or pw == "" or pw2 == "":
            flash("빈 값이 있습니다.")
            return render_template("member/modify.html", title="회원수정")
        
        if pw != pw2:
            flash("비밀번호가 다릅니다.")
            return render_template("member/modify.html", title="회원수정")
        
        if session["email"] == None or session["email"] == "":
            flash("로그인 하세요")
            return redirect(url_for("member.member_login"))

        members = mongo.db.members

        up = members.update({"_id":ObjectId(session["id"])},
                            {"$set":
                                {
                                    "name":name,
                                    "pw":pw    
                                }
                            })
        
        session["name"] = name
        return render_template("member/modify.html", title="회원수정")

    else:
        return render_template("member/modify.html",title="회원수정")



@members_blueprint.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for("home"))