import sys

import settings
from charts.classes import Chart
from database.database import Database


def get_database_params():
    """Получение параметров для подключения к базе данных"""
    # Последовательность параметров: имя БД, имя пользователя, пароль, хост, порт
    try:
        db_name, user_name, password, host, port = sys.argv[1::]
    except Exception:
        db_name = settings.DB_NAME
        user_name = settings.USER_NAME
        password = settings.PASSWORD
        host = settings.HOST
        port = settings.PORT

    table_name = settings.TABLE_NAME

    db_params = {
        'database': db_name,
        'user': user_name,
        'password': password,
        'host': host,
        'port': port,
        'table_name': table_name
    }
    return db_params


if __name__ == '__main__':
    db_params = get_database_params()
    database = Database(**db_params)
    db_data = database.extract_table_data()
    charts_data = Chart(db_data)
    charts_data.show_chart()
