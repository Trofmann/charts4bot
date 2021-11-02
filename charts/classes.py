from matplotlib import pyplot, widgets

from charts.const import WINDOW_WIDTH, WINDOW_HEIGHT, FILTER_START_LEFT, FILTER_START_TOP, ALL_LABEL
from charts.filters import filter_by_datetime_field, filter_by_json_field, filter_by_field
from const import TABLE_FIELDS, FIELDS_TYPES, DATETIME, JSON, DAY, REG_TIME, TIMEDELTAS, UNIVERSITY_ID, \
    UNIVERSITIES_CODES, UNIVERSITY_DATA, FACULTY, UNIVERSITIES_DECODES
from utils import trim_datetime, fill_by_sequential_values, is_field_type
from matplotlib import pyplot, widgets

from charts.const import WINDOW_WIDTH, WINDOW_HEIGHT, FILTER_START_LEFT, FILTER_START_TOP, ALL_LABEL
from charts.filters import filter_by_datetime_field, filter_by_json_field, filter_by_field
from const import TABLE_FIELDS, FIELDS_TYPES, DATETIME, JSON, DAY, REG_TIME, TIMEDELTAS, UNIVERSITY_ID, \
    UNIVERSITIES_CODES, UNIVERSITY_DATA, FACULTY, UNIVERSITIES_DECODES
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
        self.pyplot = pyplot
        # Параметры окна
        self.__figure = self.pyplot.figure(figsize=(WINDOW_WIDTH, WINDOW_HEIGHT))
        self__ax = self.__figure.subplots()
        # Фильтры
        self.filters = {}
        # self.rax1 = self.__figure.add_subplot([FILTER_START_LEFT, 0.7, 0.05, 0.08])
        self.university_filter1 = None
        self.un_w_r = True

    @property
    def is_empty(self):
        return bool(len(self.__rows))

    def get_users_amount(self, times, field_name=REG_TIME, trim=DAY):
        """
        Количество пользователей
        :param times: даты, для которых считаем пользователей
        :param field_name: имя поля, по которому считаем пользователей
        :param trim: момент даты, до который сравниваем
        :return: users_amounts: количества пользователей
        """
        users_amounts = []
        if FIELDS_TYPES.get(field_name, None) != DATETIME:
            print("Считать количество пользователей можно только для полей типа datetime")
            return users_amounts
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
            for row in self.__rows:
                trimmed_date = trim_datetime(getattr(row, field_name, None), trim)
                if trimmed_date not in values:
                    values.append(trimmed_date)
            values.sort()
        for row in self.__rows:
            # Необходимо для формирования баттонов на графике
            values.append(getattr(row, field_name, None))
            values = list(set(values))
            values.sort()

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
        line1 = self.pyplot.plot(self.__times, self.__users_amounts)

    def get_university_labels(self):
        """Получение значения Radio-button для фильтра university_id"""
        labels = [ALL_LABEL]
        university_ids = self.extract_field_unique_values(UNIVERSITY_ID)
        for university_id in university_ids:
            labels.append(UNIVERSITIES_CODES.get(university_id))
        return labels

    def get_faculty_labels(self, university_id):
        """Получение значения Radio-button для фильтра факультета"""
        labels = []
        for row in self.__rows:
            if getattr(row, UNIVERSITY_ID, university_id) == university_id:
                university_data = getattr(row, UNIVERSITY_DATA, None)
                if university_data:
                    label = university_data.get(FACULTY, None)
                    labels.append(label)
        return list(set(labels))

    def prepare_filters(self):
        # Фильтр университетов
        rax = self.pyplot.axes([FILTER_START_LEFT, FILTER_START_TOP, 0.05, 0.08])
        self.filters[UNIVERSITY_ID] = Filter(widgets.RadioButtons(rax, self.get_university_labels(), active=0), False)
        self.filters[UNIVERSITY_ID].widget.on_clicked(self.toggle_university_filter)

        # TODO: автоматическая генерация координат фигуры
        # Фильтр факультетов
        rax1 = self.pyplot.axes([FILTER_START_LEFT, 0.2, 0.1, 0.3])
        self.filters[FACULTY] = Filter(widget=widgets.CheckButtons(rax1, []), removed=True)
        self.filters[FACULTY].widget.ax.remove()

    def show_chart(self):
        """Вывод графиков"""
        self.prepare_data(trim=DAY)
        self.prepare_filters()

        self.pyplot.show()

    def toggle_university_filter(self, label):
        if label != ALL_LABEL:
            if self.filters[FACULTY].removed:
                rax1 = self.pyplot.axes([FILTER_START_LEFT, 0.2, 0.1, 0.3])
                university_id = UNIVERSITIES_DECODES.get(label)
                faculty_labels = self.get_faculty_labels(university_id)
                self.filters[FACULTY].widget = widgets.CheckButtons(rax1, faculty_labels)
                self.filters[FACULTY].removed = False
        else:
            self.filters[FACULTY].widget.ax.remove()
            self.filters[FACULTY].removed = True
        self.pyplot.show()

        print(label)


class Filter:
    def __init__(self, widget: widgets, removed: bool):
        self.widget = widget
        self.removed = removed
