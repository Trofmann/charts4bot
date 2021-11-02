from datetime import datetime

from const import DAY, YEAR, MONTH, HOUR, MINUTE, SECOND, FIELDS_TYPES


def tuple_to_dict(data_tuple: tuple, keys: list):
    """
    Преобразование кортежа в словарь

    :returns {keys[i] : tuple[i]}
    """
    data_dict = {}
    if len(data_tuple) != len(keys):
        print("Количество элементов кортежа не совпадает с количеством ключей")
        return data_tuple
    else:
        for ind, data in enumerate(data_tuple):
            data_dict.update({keys[ind]: data})
        return data_dict


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


def is_field_type(field, field_type):
    """Проверка на совпадение типа поля с переданном типом"""
    return FIELDS_TYPES.get(field, None) == field_type

def get_faculty_values(row):
    """Значение поля faculty"""

