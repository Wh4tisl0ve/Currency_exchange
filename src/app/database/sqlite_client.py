import sqlite3
from sqlite3 import IntegrityError

from src.app.exceptions.constraint_violation_exception import ConstraintViolationException
from src.app.exceptions.database_error import DataBaseError
from src.app.database.db_client import DBClient


class SQLiteClient(DBClient):
    def open_connection(self) -> None:
        if self.__is_connection_open():
            return
        self._connection = sqlite3.connect(self._config['sqlite']['database_path'])

    def close_connection(self) -> None:
        if self.__is_connection_open():
            self._connection.close()
            self._connection = None
        else:
            raise DataBaseError('Подключение к БД было закрыто', 500)

    def __is_connection_open(self) -> bool:
        return self._connection is not None

    def _execute_query(self, query: str, parameters: tuple = ()) -> list:
        cursor = self._connection.cursor()
        try:
            cursor.execute(query, parameters)
        except IntegrityError:
            raise ConstraintViolationException('Нарушение ссылочной целостности', 409) from IntegrityError
        return cursor.fetchall()

    def execute_ddl(self, query: str, parameters: tuple = ()) -> None:
        if self.__is_connection_open():
            self._execute_query(query, parameters)
            self._connection.commit()
        else:
            raise DataBaseError('Подключение к БД было закрыто', 500)

    def execute_dml(self, query: str) -> list:
        if self.__is_connection_open():
            return self._execute_query(query)
        else:
            raise DataBaseError('Подключение к БД было закрыто', 500)