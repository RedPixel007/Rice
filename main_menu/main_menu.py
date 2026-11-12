import json, os
from pathlib import Path

from dotenv import load_dotenv

from flask import Flask, render_template,session
from query_bp.route import blueprint_query
from auth_bp.route import blueprint_auth
from business_bp.route import blueprint_plan
from access import login_required

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    static_folder=str(BASE_DIR.parent / 'static'),
    static_url_path='/static'
)

load_dotenv(BASE_DIR.parent / ".env")
app.secret_key = os.environ["FLASK_SECRET_KEY"]

app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_plan, url_prefix='/plan')



with open('../data/db_config.json', 'r') as f:
    app.config["db_config"] = json.load(f)
with open('../data/access.json', 'r') as f:
    app.config["db_access"] = json.load(f)

@app.route('/')
@login_required
def main_menu():
    return render_template('main_menu.html', user_name = session['user_group'],access = app.config["db_access"][session['user_group']])

@app.route('/exit')
def exit_func():
    session.clear()
    return render_template('exit.html')

if __name__ == '__main__':
    app.run(debug=True)