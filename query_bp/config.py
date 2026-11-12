import json
from pathlib import Path
from flask import session

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / 'data'


with open(CONFIG_PATH/'query_data'/'query_config.json', 'r', encoding='utf-8') as file:
    QUERY_CONFIG = json.load(file)
    keys_list = list(QUERY_CONFIG.keys())

with open(CONFIG_PATH/'query_data'/'query_form.json', 'r', encoding='utf-8') as file:
    QUERY_FORM = json.load(file)

with open(CONFIG_PATH/'query_data'/'query_result.json', 'r', encoding='utf-8') as file:
     QUERY_RESULT = json.load(file)



CONFIG_PATH = BASE_DIR / 'data' / 'plan_data'

with open(CONFIG_PATH/'plan_query_config.json', 'r', encoding='utf-8') as file:
    PLAN_QUERY = json.load(file)

with open(CONFIG_PATH/'plan_query_result.json', 'r', encoding='utf-8') as file:
    PLAN_RESULT = json.load(file)

with open(CONFIG_PATH/'plan_query_form.json', 'r', encoding='utf-8') as file:
    PLAN_FORM = json.load(file)

with open(CONFIG_PATH/'plan_process_form.json', 'r', encoding='utf-8') as file:
    PLAN_PROCESS = json.load(file)