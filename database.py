import psycopg2


class Database:
    def __init__(self, **kwargs):
        self.__name = kwargs['db_name']  # type: str
        self.__user = kwargs['user']  # type: str
        self.__password = kwargs['password']  # type: str
        self.__host = kwargs['host']  # type: str
        self.__port = kwargs['port']  # type: str
        self.__table_name = kwargs['table_name']  # type: str

    def get_connection_data(self):
        return {
            'db_name': self.__name,
            'user': self.__user,
            'password': self.__password,
            'host': self.__host,
            'port': self.__port,
        }

    def connect(self):
        try:
            connection_data = self.get_connection_data()
            connection = psycopg2.connect(**connection_data)
            return connection
        except Exception:
            print('Проверь правильность данных')
            exit()

