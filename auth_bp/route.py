from flask import Flask, render_template, Blueprint, request, redirect, url_for, session

from auth_bp.model_route import model_route
from database.sql_provider import SQLProvider
from os import path

blueprint_auth = Blueprint('auth_bp', __name__, template_folder='templates')
provider = SQLProvider(path.join(path.dirname(__file__), 'sql'))


@blueprint_auth.route('/', methods=['GET', 'POST'])
def auth_index():
    func = request.args.get('func',request.form.get('func', 'main_menu'))
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        params = dict(request.form)
        response = model_route(provider, params)
        if response.status:
            query_id = request.args.get(
                'query_id', request.form.get('query_id')
            )
            return redirect(url_for(func, query_id=query_id))
        else:
            return "Не верный логин или пароль"