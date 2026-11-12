from flask import Flask, render_template, current_app, Blueprint, request, redirect, url_for, session
from database.sql_provider import SQLProvider
from os import path
from database.select import select_list, select_dict
from query_bp.config import PLAN_QUERY, PLAN_RESULT, PLAN_FORM, PLAN_PROCESS
from business_bp.model_route import model_route

from access import login_required, group_required

blueprint_plan = Blueprint('plan_bp', __name__, template_folder='templates')
provider = SQLProvider(path.join(path.dirname(__file__), 'sql'))


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
        response = model_route(provider, query_info, {})
        column_name = PLAN_RESULT[query_id]['column']
        print("Ответ:",response)
        return render_template("plan_dynamic.html", html_title=title , answer=response.result, column = column_name, user_name = session['user_group'])


@blueprint_plan.route('/query', methods=['POST'])
@login_required
@group_required
def query_executor():
    print("Suda")
    query_id = request.args.get('query_id')

    query_info = PLAN_QUERY[query_id]
    title = PLAN_QUERY[query_id]['Title']
    column_name = PLAN_RESULT[query_id]['column']

    params = dict(request.form)
    response = model_route(provider, query_info, params)

    if response.status:
        return render_template("plan_dynamic.html", html_title=title , answer=response.result, column = column_name, user_name = session['user_group'])
    else:
        return f'Что-то пошло не так, {response.err_message}'

@blueprint_plan.route('/new', methods=['GET', 'POST'])
@login_required
@group_required
def new_plan():
    if request.method == 'GET':
        print(PLAN_PROCESS)
        return render_template("basket_order_list.html", user_name = session['user_group'], plan = PLAN_PROCESS, basket = {})
    else:
        info = dict(request.form)
        key = list(info.keys())[0]

        print("prev del",session['basket'])

        if "remove" in info:
            del session["basket"][key]
            return render_template("basket_order_list.html", user_name=session['user_group'], plan=PLAN_PROCESS,basket=session["basket"])

        print("after del",session['basket'])

        print("info",info)

        if PLAN_PROCESS[key]["type"] == "bool":
            info[key] = request.form.getlist(key)[-1]
            print("info key", info[key], info)
            session['basket'][key] = info[key]
            print("update",session['basket'])

        session['basket'] = session.get('basket', {})
        session['basket'][key] = info[key]
        session.permanent = True

        print("До рендера", session['basket'])

        return render_template("basket_order_list.html",user_name = session['user_group'], plan = PLAN_PROCESS, basket = session["basket"])

def add_to_basket(item, prod_id):
    current_basket = session.get('basket', {})
    if prod_id in current_basket:
        current_basket[prod_id]['amount'] += 1
    else:
        current_basket[prod_id] = {
            'prod_name': item['prod_name'],
            'prod_price': item['prod_price'],
            'amount': 1
        }
        session['basket'] = current_basket
        session.permanent = True
    return True


@blueprint_plan.route('/new/clear', methods=['GET'])
@login_required
@group_required
def clear_basket():
    session['basket'] = {}
    PLAN_PROCESS["have_unlimit"]["value"] = "Нет"
    PLAN_PROCESS["have_stepped_volume"]["value"] = "Нет"
    print("Clear",session['basket'])
    return redirect(url_for("plan_bp.new_plan"))