# Поля, из которых извлекаем данные

from dateutil.relativedelta import relativedelta

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

TIMEDELTAS = {
    YEAR: relativedelta(years=1),
    MONTH: relativedelta(months=1),
    DAY: relativedelta(days=1),
    HOUR: relativedelta(hours=1),
    MINUTE: relativedelta(minutes=1),
    SECOND: relativedelta(minutes=1)
}
