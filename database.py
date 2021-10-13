import psycopg2

from const import TABLE_FIELDS, TABLE_NAME


class Database:
    def __init__(self, **kwargs):
        self.__name = kwargs['database']  # type: str
        self.__user = kwargs['user']  # type: str
        self.__password = kwargs['password']  # type: str
        self.__host = kwargs['host']  # type: str
        self.__port = kwargs['port']  # type: str
        self.__table_name = kwargs['table_name']  # type: str
        self.__connection = None

    def _get_connection_data(self):
        return {
            'database': self.__name,
            'user': self.__user,
            'password': self.__password,
            'host': self.__host,
            'port': self.__port,
        }

    def _connect(self):
        # Подлючение к базе данных
        try:
            connection_data = self._get_connection_data()
            self.__connection = psycopg2.connect(**connection_data)
            print('Database base was opened successfully')
        except Exception:
            print('Проверь правильность данных')
            exit()

    @staticmethod
    def _form_query():
        return 'SELECT {fields} from public."{table_name}"'.format(
            fields=', '.join(TABLE_FIELDS),
            table_name=TABLE_NAME
        )

    def extract_table_data(self):
        # Получаем данные таблицы
        if self.__connection is None or self.__connection.closed:
            self._connect()
        query = self._form_query()
        cursor = self.__connection.cursor()
        cursor.execute(query)

        data = cursor.fetchall()
        print('Data was extracted')
        return data
