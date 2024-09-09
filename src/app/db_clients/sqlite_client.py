from src.app.exceptions.constraint_violation_error import ConstraintViolationException
from src.app.exceptions.db_error.database_error import DataBaseError
from src.app.exceptions.not_found_error import NotFoundError
from src.app.db_clients.config.config import load_config
from src.app.db_clients.db_client import DBClient
from sqlite3 import IntegrityError, OperationalError, DatabaseError
import sqlite3


class SQLiteClient(DBClient):
    def __init__(self):
        super().__init__()
        self.__config = load_config()
        self.open_connection()

    def open_connection(self) -> None:
        if self.__is_connection_open():
            return
        try:
            self.client = sqlite3.connect(self.__config['sqlite']['database_path'])
        except OperationalError:
            raise NotFoundError('Файл базы данных не был найден')
        except DatabaseError:
            raise DataBaseError('База данных недоступна')

    def __is_connection_open(self) -> bool:
        return self.client is not None

    def _execute_query(self, query: str, parameters: tuple = ()) -> list[tuple]:
        cursor = self.client.cursor()
        try:
            cursor.execute(query, parameters)
            data = cursor.fetchall()
            cursor.close()
        except IntegrityError as e:
            raise ConstraintViolationException(e.args[0])

        return data

    def execute_ddl(self, query: str, parameters: tuple = ()) -> None:
        if self.__is_connection_open():
            self._execute_query(query, parameters)
            self.client.commit()
        else:
            raise DataBaseError('Подключение к БД было закрыто')

    def execute_dml(self, query: str, parameters: tuple = ()) -> list:
        if self.__is_connection_open():
            return self._execute_query(query, parameters)
        else:
            raise DataBaseError('Подключение к БД было закрыто')
