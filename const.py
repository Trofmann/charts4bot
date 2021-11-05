from dateutil.relativedelta import relativedelta

RED_COLOR = '\033[31m'

# Поля, из которых извлекаем данные
ID = 'id'
UNIVERSITY_ID = 'university_id'
UNIVERSITY_DATA = 'university_data'
REG_TIME = 'reg_time'
FACULTY = 'faculty'

# Извлекаемые поля
TABLE_FIELDS = [
    ID,
    UNIVERSITY_ID,
    UNIVERSITY_DATA,
    REG_TIME,
]

# Поля, которые есть в извлекаемых parent-json-полях (field: parent)
TABLE_EXTRA_FIELDS = {
    FACULTY: UNIVERSITY_DATA
}

# Типы извлекаемых полей
INTEGER = 'integer'
CHAR = 'char_field'
JSON = 'json'
DATETIME = 'timestamp'

FIELDS_TYPES = {
    ID: INTEGER,
    UNIVERSITY_ID: CHAR,
    UNIVERSITY_DATA: JSON,
    REG_TIME: DATETIME,
    FACULTY: CHAR
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

TIMEDELTAS = {
    YEAR: relativedelta(years=1),
    MONTH: relativedelta(months=1),
    DAY: relativedelta(days=1),
    HOUR: relativedelta(hours=1),
    MINUTE: relativedelta(minutes=1),
    SECOND: relativedelta(minutes=1)
}

# Поля, по которым фильтруем
FILTERING_FIELDS = [
    UNIVERSITY_ID
]
