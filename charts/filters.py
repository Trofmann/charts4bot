def filter_by_field(rows, field, values=None):
    """
    Фильрация по значениям полей любых типов кроме datetime, json
    """
    filtered_values = []
    for row in rows:
        if getattr(row, field) in values:
            filtered_values.append(row)
    return filtered_values


def filter_by_datetime_field(rows, field_name, values=None):
    """
    Фильтрация по значениям поля типа datetime
    """
    return rows


def filter_by_json_field(rows, field, values=None):
    """
    Фильтрация по значениям поля типа json
    """
    return rows
