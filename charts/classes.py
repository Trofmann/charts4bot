from matplotlib import pyplot
from matplotlib.widgets import RadioButtons, CheckButtons

from charts.const import WINDOW_WIDTH, WINDOW_HEIGHT, FILTER_START_LEFT, FILTER_START_TOP, ALL_LABEL, \
    UNIVERSITIES_DECODES, UNIVERSITIES_CODES, FACULTIES_DECODES
from charts.filters import filter_by_datetime_field, filter_by_json_field, filter_by_field
from charts.utils import trim_datetime, fill_by_sequential_values, extract_field_unique_values, get_faculty_labels, \
    code_decode_vales
from const import TABLE_FIELDS, FIELDS_TYPES, DATETIME, JSON, DAY, REG_TIME, TIMEDELTAS, UNIVERSITY_ID, \
    FACULTY
from utils import is_field_type


class Chart:
    """Класс для вывода графика"""

    def __init__(self, rows):
        # Данные, полученные из БД
        self.__rows = rows
        # Данные, которые демонстрируем (Изначально демострируем всё)
        self.__showing_rows = rows

        # Даты по оси x
        self.__times = []
        # Количество пользователей по оси y
        self.__users_amounts = []

        # График
        self.pyplot = pyplot
        self.figure, self.ax = self.pyplot.subplots(figsize=(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.figure = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.chart_line = None

        # Фильтры
        self.filters_inited = False
        self.filters = {}

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
        for value in times:
            amount = 0
            for row in self.__showing_rows:
                row_field_value = trim_datetime(getattr(row, field_name, None), trim)
                amount += int(value == row_field_value)
            users_amounts.append(amount)

        return users_amounts

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

        times = extract_field_unique_values(self.__rows, field_name=REG_TIME, trim=trim)
        _timedelta = TIMEDELTAS.get(trim, None)
        self.__times = fill_by_sequential_values(times[0], times[-1], _timedelta, _datetime=True)

        users_amount = self.get_users_amount(times=self.__times, field_name=REG_TIME, trim=trim)
        self.__users_amounts = users_amount

        if self.chart_line is None:
            self.chart_line, = self.ax.plot(self.__times, self.__users_amounts)
        else:
            self.chart_line.set_xdata(self.__times)
            self.chart_line.set_ydata(self.__users_amounts)
        self.pyplot.draw()

    def init_filters(self):
        """Подготовка фильров"""
        # Фильтр университетов
        rax = self.pyplot.axes([FILTER_START_LEFT, FILTER_START_TOP, 0.05, 0.08])
        self.filters[UNIVERSITY_ID] = Filter(RadioButtons(rax, self.get_university_labels(), active=0), False)
        self.filters[UNIVERSITY_ID].widget.on_clicked(self.toggle_university_filter)

        # Фильтр факультетов
        rax1 = self.pyplot.axes([FILTER_START_LEFT, 0.2, 0.1, 0.3])
        self.filters[FACULTY] = Filter(widget=CheckButtons(rax1, []), removed=True)
        self.filters[FACULTY].widget.ax.remove()

        self.filters_inited = True

    def get_university_labels(self):
        """Получение значения Radio-button для фильтра university_id"""
        labels = [ALL_LABEL]
        university_ids = extract_field_unique_values(self.__rows, UNIVERSITY_ID)
        for university_id in university_ids:
            labels.append(UNIVERSITIES_CODES.get(university_id))
        return labels

    def get_filters_values(self, label):
        """Получение выбранных значений фильтров"""
        sorting_values = {}
        for field_name, filter_ in self.filters.items():
            filter_chosen_values = filter_.get_chosen()
            # filter_chosen_values == None, если фильтр скрыт
            if filter_chosen_values is not None and filter_chosen_values != ALL_LABEL:
                # Переводим из человеческих слов в коды
                if field_name == UNIVERSITY_ID:
                    filter_chosen_values = code_decode_vales(UNIVERSITIES_DECODES, filter_chosen_values)

                elif field_name == FACULTY:
                    university_id = code_decode_vales(UNIVERSITIES_DECODES, self.filters[UNIVERSITY_ID].get_chosen())[0]
                    filter_chosen_values = code_decode_vales(FACULTIES_DECODES[university_id], filter_chosen_values)
                    sorting_values.update({
                        field_name: filter_chosen_values
                    })

            sorting_values.update({
                field_name: filter_chosen_values
            })
        print(f'Фильтры: {sorting_values}')
        return sorting_values

    def toggle_university_filter(self, label):
        """Обработка нажатия на фильтр университетов"""
        if label != ALL_LABEL:
            if self.filters[FACULTY].removed:
                rax1 = self.pyplot.axes([FILTER_START_LEFT, 0.2, 0.1, 0.3])
                university_id = UNIVERSITIES_DECODES.get(label)
                faculty_labels = get_faculty_labels(self.__rows, university_id)
                faculty_labels.sort()
                self.filters[FACULTY].widget = CheckButtons(rax1, faculty_labels,
                                                            actives=[True] * len(faculty_labels))
                self.filters[FACULTY].removed = False
        # Если выбрано значение "Все", скрываем фильтр факультетов
        elif not self.filters[FACULTY].removed:
            self.filters[FACULTY].widget.ax.remove()
            self.filters[FACULTY].removed = True
            # ПРИМЕР ИЗМЕНЕНИЯ
            # self.chart_line.set_xdata(self.__times[1:9])
            # self.chart_line.set_ydata(self.__users_amounts[1:9])

        self.pyplot.show()

    def show_chart(self):
        """Вывод графиков"""
        # Чтобы можно было использовать функцию при нажатии на фильтр
        if not self.filters_inited:
            self.init_filters()
        self.prepare_data(trim=DAY)

        self.pyplot.show()


class Filter:
    """Фильтр"""

    def __init__(self, widget, removed: bool):
        self.widget = widget
        self.removed = removed

    def get_chosen(self):
        """
        Получение выбранных значений фильтра
        :return: list
        """
        if not self.removed:
            if isinstance(self.widget, RadioButtons):
                return self.widget.value_selected
            elif isinstance(self.widget, CheckButtons):
                statuses = self.widget.get_status()
                labels = self.widget.labels
                return [label._text for label, status in zip(labels, statuses) if status]
            else:
                print('Обрабатываются только RadioButtons, CheckButtons')
