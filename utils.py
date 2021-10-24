from datetime import datetime

from const import DAY, YEAR, MONTH, HOUR, MINUTE, SECOND


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
