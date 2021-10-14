import sys

from charts.classes import Data
from database.database import Database
import const


def get_database_params():
    # Последовательность параметров: имя БД, имя пользователя, пароль, хост, порт
    try:
        db_name, user_name, password, host, port = sys.argv[1::]
    except Exception:
        db_name = const.DB_NAME
        user_name = const.USER_NAME
        password = const.PASSWORD
        host = const.HOST
        port = const.PORT

    table_name = const.TABLE_NAME

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
    charts_data = Data(db_data)
    print(2)
