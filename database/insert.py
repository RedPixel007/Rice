from database.DBcm import DBContextManager
from flask import current_app

def insert_sql(sql, params):
    with DBContextManager(current_app.config["db_config"]) as cursor:
        if cursor is None:
            print("Курсор не создан")
            raise ValueError("Курсор не создан")

        cursor.execute(sql, params)

        print("insert")

        print("Описание:",cursor.description)
        if cursor.description:
            return cursor.fetchone()
        return None