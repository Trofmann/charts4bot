from matplotlib import pyplot, widgets

from charts.const import WINDOW_WIDTH, WINDOW_HEIGHT
from const import TABLE_FIELDS, FIELDS_TYPES, DATETIME, JSON, DAY, REG_TIME, MONTH, MINUTE
from utils import trim_datetime


class Chart:
    """Класс для вывда графика"""

    def __init__(self, rows):
        # Данные, полученные из БД
        self.__rows = rows
        # Данные, которые демонстрируем (Изначально демострируем всё)
        self.__showing_rows = rows
        # Даты для оси x
        self.__times = []
        # Количество пользователей по оси y
        self.__users_amounts = []
        # График
        self.__ax = pyplot
        # Параметры окна
        self.__ax.figure(figsize=(WINDOW_WIDTH, WINDOW_HEIGHT))

    @property
    def is_empty(self):
        return bool(len(self.__rows))

    def get_users_amount(self, field_name=REG_TIME, trim=DAY):
        """Получение количества пользователей

        Аргументы:
        field_name - имя поля, данные которого извлекаем
        """
        self.__users_amounts = []
        if FIELDS_TYPES.get(field_name, None) != DATETIME:
            print("Считать количество пользователей можно только для полей типа datetime")
            return 0
        # Уникальные значения поля
        field_values = self.extract_field_unique_values(field_name, trim)
        for value in field_values:
            amount = 0
            for row in self.__showing_rows:
                row_field_value = trim_datetime(getattr(row, field_name, None), trim)
                amount += int(value == row_field_value)
            self.__users_amounts.append(amount)

    def extract_field_unique_values(self, field_name: str, trim=DAY):
        """
        Извлечение уникальных значений поля
        :param field_name: имя поля, данные которого извлекаем
        :param trim: in const.TRIMS
        :return: values
        """

        values = []
        # Отдельно проверяем значения поля с типом datetime.datetime
        if FIELDS_TYPES.get(field_name, None) == DATETIME:
            for row in self.__showing_rows:
                trimmed_date = trim_datetime(getattr(row, field_name, None), trim)
                if trimmed_date not in values:
                    values.append(trimmed_date)
            values.sort()
        for row in self.__showing_rows:
            # Необходимо для формирования баттонов на графике
            pass

        self.__times = values
        return values

    def filter_by_field_values(self, field_name: str, values=None):
        """
        Фильтрация данных по значениям поля
        :param field_name: имя поля
        :param values: значения
        :return: None
        """
        # TODO: додумать фильтрацию по нескольким полям
        if values is None:
            self.__showing_rows = self.__rows
            return

        self.__showing_rows = []
        if field_name not in TABLE_FIELDS:
            print("Имя поля не извлекалось из БД")
            return

        # Отдельно фильтруем поля с типом datetime.datetime
        if FIELDS_TYPES.get(field_name, None) == DATETIME:
            # TODO: добавить фильтрацию по datetime-полям
            # Не к спеху
            # Например, промежуток времени
            # Понадобится trim_datetime
            pass

        # Отдельно фильтруем поля с типом json
        if FIELDS_TYPES.get(field_name, None) == JSON:
            # TODO: добавить фльтрацию по json-полям
            pass

        for row in self.__rows:
            if getattr(row, field_name) in values:
                self.__showing_rows.append(row)

    def show_chart(self):
        # TODO: переименовать в show
        # TODO: числовые параметры фигур задать константами или вычислять автоматически
        # Вывод графиков
        self.get_users_amount(trim=DAY)
        line1 = self.__ax.plot(self.__times, self.__users_amounts)
        # rax - фигура, в которой рисуется виджет
        # TODO: в фильтре генерировать автоматически
        # rax = self.__ax.axes([0.1, 0.4, 0.1, 0.15])
        # check = widgets.CheckButtons(rax, ["asdasd", "asdasd"], )
        # check2 = widgets.RadioButtons(rax, ['dasdasda', 'asdasdasd'])
        self.__ax.show()

# TODO: создать class Filter - набор радиобаттонов и чекбаттонов, параметр иницилизации - ax
# В нём - обработка нажатия кнопки submit

# TODO: trim извлекать с помощью радиобаттонов
# TODO: подумать над динамическим фильтром
# TODO: получать минимальное значение времени, максимальное значение времени
