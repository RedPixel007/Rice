from functools import wraps
from flask import session, redirect, url_for, current_app, request
from query_bp.config import QUERY_CONFIG, PLAN_QUERY

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        query_id = request.args.get(
            'query_id', request.form.get('query_id')
        )
        if "user_group" in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("auth_bp.auth_index", func = request.endpoint, query_id = query_id))
    return wrapper


def group_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        query_id = request.args.get(
            'query_id', request.form.get('query_id')
        )
        if "user_group" in session:
            access = current_app.config["db_access"]
            user_request = request.endpoint.split('.')[0]
            user_role = session["user_group"]
            if user_role in access and user_request in access[user_role]:
                if (query_id != None and
                    (query_id in QUERY_CONFIG.keys() and user_role in QUERY_CONFIG[query_id]["group"])
                        or (query_id in PLAN_QUERY.keys() and user_role in PLAN_QUERY[query_id]["group"])) \
                            or query_id == None:

                    return func(*args, **kwargs)

                else:
                    return redirect(url_for("auth_bp.auth_index", func=request.endpoint, query_id=query_id))
            else:
                return redirect(url_for("auth_bp.auth_index", func = request.endpoint, query_id = query_id))
    return wrapper