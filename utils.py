from const import FIELDS_TYPES


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


def is_field_type(field, field_type):
    """Проверка на совпадение типа поля с переданном типом"""
    return FIELDS_TYPES.get(field, None) == field_type
