from const import TABLE_FIELDS


class Data:
    """Класс для хранения и манипулирования данными для графиков"""

    def __init__(self, rows):
        self.__rows = rows

    def get_users_amount(self, field_name: str):
        if field_name not in TABLE_FIELDS:
            print("field_name not in extracted fields")
            return 0
        # Уникальные значения поля
        field_values = []

    def extract_field_unique_values(self, field_name):
        pass