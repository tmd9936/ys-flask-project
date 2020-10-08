from functools import wraps
from flask import session, redirect, url_for, request

def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwards):
        if session.get("id") is None or session.get("id") == "":
            return redirect(url_for("member.member_login", next_url= request.url))
        return f(*args, **kwards)
    return decorated_func









