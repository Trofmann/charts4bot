import sys
from database import Database
import const


def get_params():
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

    db_data = {
        'database': db_name,
        'user': user_name,
        'password': password,
        'host': host,
        'port': port,
        'table_name': table_name
    }
    return db_data


if __name__ == '__main__':
    db_data = get_params()
    database = Database(**db_data)
    data = database.extract_table_data()
    print(data)

    #
    # connection_cursor = connection.cursor()
    # connection.close()
    # print(1)
