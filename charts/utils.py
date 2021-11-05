from datetime import datetime

from charts.const import FACULTIES_DECODES
from const import YEAR, DAY, MONTH, HOUR, MINUTE, SECOND, FIELDS_TYPES, DATETIME, JSON, TABLE_EXTRA_FIELDS, RED_COLOR


def trim_datetime(_datetime, trim=DAY):
    """
    Очистка даты до определенного момента
    :param _datetime: datetime.datetime
    :param trim: str
    :return: datetime
    """
    clean_datetime = None
    if _datetime:
        clean_datetime = datetime(_datetime.year, _datetime.month, _datetime.day)
        if trim == YEAR:
            clean_datetime = clean_datetime.replace(month=1, day=1)
        elif trim == MONTH:
            clean_datetime = clean_datetime.replace(day=1)
        elif trim == HOUR:
            clean_datetime = clean_datetime.replace(hour=_datetime.hour)
        elif trim == MINUTE:
            clean_datetime = clean_datetime.replace(hour=_datetime.hour, minute=_datetime.minute)
        elif trim == SECOND:
            clean_datetime = clean_datetime.replace(hour=_datetime.hour, minute=_datetime.minute,
                                                    second=_datetime.second)
    return clean_datetime


def fill_by_sequential_values(start_val, stop_val, step, _datetime=False):
    """
    Последовательные значения
    :param start_val: начальное значение
    :param stop_val: конечное значение
    :param step: шаг
    :param _datetime: флаг
    :return: list
    """
    values = []
    if _datetime:
        current_datetime = start_val
        while current_datetime <= stop_val:
            values.append(current_datetime)
            current_datetime = current_datetime + step
    else:
        values = [i for i in range(start_val, stop_val + step, step)]
    return values


def extract_field_unique_values(rows, field_name: str, trim=DAY):
    """
    Извлечение уникальных значений поля
    :param rows: значения поля
    :param field_name: имя поля, данные которого извлекаем
    :param trim: in const.TRIMS
    :return: values
    """

    values = []
    if FIELDS_TYPES.get(field_name, None) == JSON:
        print('Уникальные значения полей с типом json извлекаются другой функцией')
    # Отдельно проверяем значения поля с типом datetime.datetime
    elif FIELDS_TYPES.get(field_name, None) == DATETIME:
        for row in rows:
            trimmed_date = trim_datetime(getattr(row, field_name, None), trim)
            if trimmed_date not in values:
                values.append(trimmed_date)
        values.sort()
    else:
        for row in rows:
            # Необходимо для формирования баттонов на графике
            values.append(getattr(row, field_name, None))
            values = list(set(values))
            values.sort()

    return values


def get_faculty_labels(university_id):
    """Получение значения Radio-button для фильтра факультета"""
    return [label for label in FACULTIES_DECODES.get(university_id)]


def code_decode_vales(dict_, rows):
    """Из человеческих слов в коды или наоборот"""
    # На случай RadioButton
    if not isinstance(rows, list):
        rows = [rows]
    values_ = []
    for value in rows:
        code_ = dict_.get(value, None)
        if code_:
            values_.append(code_)
        else:
            print(f'Значение {code_} не найдено в словаре')
    return values_


def get_extra_field_parent_field(field):
    """Получение родительского json-поля"""
    parent_field = TABLE_EXTRA_FIELDS.get(field, None)
    if parent_field:
        return parent_field
    print(f'{RED_COLOR}Поля {field} не является полей json-поля')
