import sys
from database import Database


def get_params():
    # Последовательность параметров: имя БД, имя пользователя, пароль, хост, порт
    try:
        db_name, user_name, password, host, port = sys.argv[1::]
    except Exception:
        db_name = 'd4j4mnjl0qr8lh'
        user_name = 'postgres'
        password = 'postgres'
        host = '127.0.0.1'
        port = '5432'

    table_name = 'TCUserData'

    db_data = {
        'db_name': db_name,
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
    print(1)

    #
    # connection_cursor = connection.cursor()
    # connection.close()
    # print(1)
