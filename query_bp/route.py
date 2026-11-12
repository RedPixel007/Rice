from flask import Flask, render_template, Blueprint, request,session
from database.select import select_dict
from database.sql_provider import SQLProvider
from os import path
from query_bp.model_route import model_route
from query_bp.config import QUERY_CONFIG,QUERY_FORM,QUERY_RESULT, keys_list
from access import login_required, group_required

blueprint_query = Blueprint('query_bp', __name__, template_folder='templates')
provider = SQLProvider(path.join(path.dirname(__file__), 'sql'))


@blueprint_query.route('/')
@login_required
@group_required
def query_menu_handler():
    return render_template('query_menu.html',group = session["user_group"], query_form = QUERY_FORM, config = QUERY_CONFIG, keys = keys_list, user_name = session['user_group'])


@blueprint_query.route('/execute', methods=['GET'])
@login_required
@group_required
def query_handler():
    query_id = request.args.get(
        'query_id',
        request.form.get('query_id', 'client')
    )
    query_info = QUERY_CONFIG[query_id]

    query_form = QUERY_FORM[query_id]
    query_field = query_form.get("query_field")

    return render_template('query.html', query_name=query_info.get('title'), query=query_field, user_name = session['user_group'])

@blueprint_query.route('/execute', methods=['POST'])
@login_required
@group_required
def query_executor():
    query_id = request.args.get(
        'query_id',
        request.form.get('query_id', 'client')
    )

    query_info = QUERY_CONFIG[query_id]
    title = query_info.get("title")
    query_col = QUERY_RESULT[query_id]
    column_name = query_col.get("column")

    params = dict(request.form)
    print(params)
    response = model_route(provider, query_info, params)

    if response.status:
        return render_template("dynamic.html", html_title=title , answer=response.result, column = column_name, user_name = session['user_group'])
    else:
        return f'Что-то пошло не так, {response.err_message}'
