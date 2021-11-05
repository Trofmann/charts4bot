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


def filter_by_json_field(rows, field, parent_json_field, values=None):
    """
    Фильтрация по значениям поля типа json
    """
    filtered_rows = []
    for row in rows:
        parent_field_row = getattr(row, parent_json_field, None)
        if parent_field_row is not None:
            field_value = parent_field_row.get(field, None)
            if field_value in values:
                filtered_rows.append(row)
    return filtered_rows
