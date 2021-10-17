from const import TABLE_FIELDS, FIELDS_TYPES, DATETIME


class Data:
    """Класс для хранения и манипулирования данными для графиков"""

    def __init__(self, rows):
        # Данные
        self.__rows = rows
        # Даты для оси x
        self.__times = []

    @property
    def is_empty(self):
        return bool(len(self.__rows))

    def get_users_amount(self, field_name: str):
        """Получение количества пользователей"""
        if field_name not in TABLE_FIELDS:
            print("field_name not in extracted fields")
            return 0
        # Уникальные значения поля
        field_values = []

    def extract_field_unique_values(self, field_name: str):
        """Извлечение уникальных значений поля"""
        # Отдельно проверяем значения поля с типом datetime.datetime
        if FIELDS_TYPES.get(field_name, None) == DATETIME:
            pass
        pass

    def clean_datetime_field(self, field_name, trim):
        """Очистка даты до дня"""
        pass
