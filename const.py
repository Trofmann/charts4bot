# Данные базы данных
DB_URL = ''
TEST_DB_NAME = 'test_d4j4mnjl0qr8lh'
DB_NAME = 'd4j4mnjl0qr8lh'
USER_NAME = 'postgres'
PASSWORD = 'postgres'
HOST = '127.0.0.1'
PORT = '5432'
TABLE_NAME = 'TCUserData'

# Поля, из которых извлекаем данные
ID = 'id'
UNIVERSITY_ID = 'university_id'
UNIVERSITY_DATA = 'university_data'
REG_TIME = 'reg_time'

TABLE_FIELDS = [
    ID,
    UNIVERSITY_ID,
    UNIVERSITY_DATA,
    REG_TIME
]

# Типы извлекаемых полей
INTEGER = 'integer'
CHAR = 'field'
JSON = 'json'
DATETIME = 'timestamp'

FIELDS_TYPES = {
    'id': INTEGER,
    'university_id': CHAR,
    'university_data': JSON,
    'reg_time': DATETIME,
}

# Моменты, до которых берем дату
YEAR = 'year'
MONTH = 'month'
DAY = 'day'
HOUR = 'hour'
MINUTE = 'minute'
SECOND = 'second'

TRIMS = [
    YEAR,
    MONTH,
    DAY,
    HOUR,
    MINUTE,
    SECOND
]

# Для фильтрации данных
COUNT = 'count'
SHOW = 'show'

REASONS = [
    COUNT,
    SHOW
]