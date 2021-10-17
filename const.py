# Данные базы данных
DB_NAME = 'd4j4mnjl0qr8lh'
USER_NAME = 'postgres'
PASSWORD = 'postgres'
HOST = '127.0.0.1'
PORT = '5432'
TABLE_NAME = 'TCUserData'

# Поля, из которых извлекаем данные
TABLE_FIELDS = [
    'id',
    'university_id',
    'university_data',
    'reg_time'
]

INTEGER = 'integer'
CHAR = 'field'
JSON = 'json'
DATETIME = 'timestamp'

# Типы извлекаемых полей
FIELDS_TYPES = {
    'id': INTEGER,
    'university_id': CHAR,
    'university_data': JSON,
    'reg_time': DATETIME,
}

