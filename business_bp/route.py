from flask import Flask, render_template, current_app, Blueprint, request, redirect, url_for, session
from database.sql_provider import SQLProvider
from os import path
from database.select import select_list, select_dict
from query_bp.config import PLAN_QUERY, PLAN_RESULT, PLAN_FORM, PLAN_PROCESS
from business_bp.model_route import model_route_sel, model_route_ins

from access import login_required, group_required

blueprint_plan = Blueprint('plan_bp', __name__, template_folder='templates')
provider = SQLProvider(path.join(path.dirname(__file__), 'sql'))
basket_def = {
    "have_unlimit": "Нет",
    "have_stepped_volume": "Нет"
             }


@blueprint_plan.route('/', methods=['GET'])
@login_required
@group_required
def tariff_page():
    keys = list(PLAN_QUERY.keys())
    return render_template('plan_main_menu.html',keys = keys, dict=PLAN_QUERY, user_name = session["user_group"])

@blueprint_plan.route('/query', methods=['GET'])
@login_required
@group_required
def query_handler():
    query_id = request.args.get('query_id')

    query_info = PLAN_QUERY[query_id]
    title = PLAN_QUERY[query_id]['Title']


    if PLAN_QUERY[query_id]["need_form"] == "True":
        query_field = PLAN_FORM[query_id]["query_field"]
        return render_template('plan_query.html', query_name=title, query=query_field, user_name = session['user_group'])
    else:
        response = model_route_sel(provider, query_info, {})
        column_name = PLAN_RESULT[query_id]['column']
        print("Ответ:",response)
        return render_template("plan_dynamic.html", html_title=title , answer=response.result, column = column_name, user_name = session['user_group'])


@blueprint_plan.route('/query', methods=['POST'])
@login_required
@group_required
def query_executor():
    query_id = request.args.get('query_id')

    query_info = PLAN_QUERY[query_id]
    title = PLAN_QUERY[query_id]['Title']
    column_name = PLAN_RESULT[query_id]['column']

    params = dict(request.form)
    response = model_route_sel(provider, query_info, params)

    if response.status:
        return render_template("plan_dynamic.html", html_title=title , answer=response.result, column = column_name, user_name = session['user_group'])
    else:
        return f'Что-то пошло не так, {response.err_message}'

@blueprint_plan.route('/new', methods=['GET', 'POST'])
@login_required
@group_required
def new_plan():
    if request.method == 'GET':
        session['basket_full'] = session.get('basket_full', 'False')
        print(session["basket_full"])
        print(list(PLAN_PROCESS.keys()))
        print(list(session["basket"].keys()))
        return render_template("basket_order_list.html",user_name = session['user_group'], plan = PLAN_PROCESS,
                               basket = session["basket"], keys = list(PLAN_PROCESS.keys()), basket_full = session["basket_full"])
    else:
        info = dict(request.form)
        key = list(info.keys())[0]

        session['basket_full'] = session.get('basket_full', "False")

        if "remove" in info and key in session["basket"]:
            session['basket_full'] = "False"
            del session["basket"][key]
            return render_template("basket_order_list.html", user_name=session['user_group'], plan=PLAN_PROCESS,
                                   basket=session["basket"], keys=list(PLAN_PROCESS.keys()), basket_full = session["basket_full"])

        if PLAN_PROCESS[key]["type"] == "bool":
            info[key] = request.form.getlist(key)[-1]
            session['basket'][key] = info[key]

        session['basket'] = session.get('basket', basket_def)
        session['basket'][key] = info[key]
        session.permanent = True
        print("Перед If")

        for key in list(PLAN_PROCESS.keys()):
            print("for")
            if key not in session["basket"]:
                if (key == 'min_volume' or key == 'step_volume') and session["basket"]["have_stepped_volume"] == "Нет":
                    continue
                session['basket_full'] = "False"
                print("No", key, session["basket"])
                break
            session['basket_full'] = "True"

        print(session['basket_full'])
        print(list(PLAN_PROCESS.keys()))
        print(list(session['basket'].keys()))
        print(session["basket"])
        return render_template("basket_order_list.html",user_name = session['user_group'], plan = PLAN_PROCESS, basket = session["basket"], basket_full = session['basket_full'] )


@blueprint_plan.route('/new/clear', methods=['GET'])
@login_required
@group_required
def clear_basket():
    session['basket'] = basket_def
    del session['basket_full']
    return redirect(url_for("plan_bp.new_plan"))



@blueprint_plan.route('/new/create', methods=['GET'])
@login_required
@group_required
def create_plan():
    params = []
    if session["basket"]["have_stepped_volume"] == "Нет":
        session["basket"]["min_volume"] = session["basket"]["max_volume"]
        session["basket"]["step_volume"] = '0'
    for key in list(PLAN_PROCESS.keys()):
        params.append(session["basket"][key])

    query_info = PLAN_QUERY["new_plan"]
    title = query_info["Title"]

    column_name = PLAN_RESULT["new_plan"]["column"]

    response = model_route_ins(provider, query_info, params)

    result = model_route_sel(provider, query_info, {"1":response.result[0]})

    print(result)

    if result.status:
        session["basket"] = basket_def
        del session["basket_full"]
        return render_template("plan_dynamic.html", html_title=title , answer=result.result, column = column_name, user_name = session['user_group'])
    else:
        return f'Что-то пошло не так, {response.err_message}'