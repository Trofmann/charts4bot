from matplotlib import pyplot

from charts.const import WINDOW_WIDTH, WINDOW_HEIGHT
from charts.filters import filter_by_datetime_field, filter_by_json_field, filter_by_field
from const import TABLE_FIELDS, FIELDS_TYPES, DATETIME, JSON, DAY, REG_TIME, TIMEDELTAS
from utils import trim_datetime, fill_by_sequential_values, is_field_type


class Chart:
    """Класс для вывода графика"""

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

    def get_users_amount(self, times, field_name=REG_TIME, trim=DAY):
        """

        :param times: даты, для которых считаем пользователей
        :param field_name: имя поля, по которому считаем пользователей
        :param trim: момент даты, до который сравниваем
        :return: users_amounts: количества пользователей
        """
        users_amounts = []
        if FIELDS_TYPES.get(field_name, None) != DATETIME:
            print("Считать количество пользователей можно только для полей типа datetime")
            return 0
        # Уникальные значения поля
        for value in times:
            amount = 0
            for row in self.__showing_rows:
                row_field_value = trim_datetime(getattr(row, field_name, None), trim)
                amount += int(value == row_field_value)
            users_amounts.append(amount)

        return users_amounts

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

        return values

    def filter_by_fields_values(self, values=None, **kwargs):
        """
        Фильтрация данных по значениям поля
        :param values: значения
        :param kwargs: словарь вида {имя_поля : [значения]}
        :return: filtered_values: список отфильтрованных значений
        """

        filtered_values = self.__rows
        for field, values in kwargs.items():
            if field not in TABLE_FIELDS:
                print(f'Поле {field} не извлекалось из БД')
                continue
            if not isinstance(values, list):
                values = [values]
                print(f'Для поля {field} передан не список значений: ({values})')

            if is_field_type(field, DATETIME):
                filtered_values = filter_by_datetime_field(filtered_values, field, values)
            elif is_field_type(field, JSON):
                filtered_values = filter_by_json_field(filtered_values, field, values)
            else:
                filtered_values = filter_by_field(filtered_values, field, values)

        return filtered_values

    def prepare_data(self, trim=DAY):
        """Подготовка данных к выводу"""
        times = self.extract_field_unique_values(field_name=REG_TIME, trim=trim)
        _timedelta = TIMEDELTAS.get(trim, None)
        self.__times = fill_by_sequential_values(times[0], times[-1], _timedelta, _datetime=True)

        users_amount = self.get_users_amount(times=self.__times, field_name=REG_TIME, trim=trim)
        self.__users_amounts = users_amount

    def show_chart(self):
        # TODO: числовые параметры фигур задать константами или вычислять автоматически
        # Вывод графиков
        self.prepare_data(trim=DAY)
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
