from const import TABLE_FIELDS, FIELDS_TYPES, DATETIME


class Data:
    """Класс для хранения и манипулирования данными для графиков"""

    def __init__(self, rows):
        # Данные, полученные из БД
        self.__rows = rows
        # Данные, которые демонстрируем (Изначально демострируем всё)
        self.__showing_rows = rows
        # Даты для оси x
        self.__times = []

    @property
    def is_empty(self):
        return bool(len(self.__rows))

    def get_users_amount(self, field_name: str):
        """Получение количества пользователей

        Аргументы:
        field_name - имя поля, данные которого извлекаем
        """
        if field_name not in TABLE_FIELDS:
            print("field_name not in extracted fields")
            return 0
        # Уникальные значения поля
        field_values = []

    def extract_field_unique_values(self, field_name: str, trim):
        """
        Извлечение уникальных значений поля
        :param field_name: имя поля, данные которого извлекаем
        :param trim: in const.TRIMS
        :return:
        """

        values = set()
        # Отдельно проверяем значения поля с типом datetime.datetime
        if FIELDS_TYPES.get(field_name, None) == DATETIME:
            pass
        for row in self.__rows:
            pass

    def filter_by_field_values(self, field_name: str, values=None):
        """
        Фильтрация данных по значениям поля
        :param field_name: имя поля
        :param values: значения
        :return: None
        """
        if values is None:
            self.__showing_rows = self.__rows
            return

        self.__showing_rows = []
        if field_name not in TABLE_FIELDS:
            print("Имя поля не извлекалось из БД")
            return

        # Отдельно проверяем поля с типом datetime.datetime
        if FIELDS_TYPES.get(field_name, None) == DATETIME:
            # Понадобится trim_datetime
            pass

        for row in self.__rows:
            if getattr(row, field_name) in values:
                self.__showing_rows.append(row)
        print(1)