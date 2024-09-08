from src.app.exceptions.db_error.database_file_not_found_error import DatabaseFileNotFoundError
from src.app.exceptions.constraint_violation_error import ConstraintViolationException
from src.app.exceptions.db_error.database_error import DataBaseError
from src.app.database.db_client import DBClient
from sqlite3 import IntegrityError, OperationalError, DatabaseError
import sqlite3


class SQLiteClient(DBClient):
    def open_connection(self) -> None:
        if self.__is_connection_open():
            return
        try:
            self._connection = sqlite3.connect(self._config['sqlite']['database_path'])
        except OperationalError:
            raise DatabaseFileNotFoundError('Файл базы данных не был найден')
        except DatabaseError:
            raise DataBaseError('База данных недоступна')

    def close_connection(self) -> None:
        if self.__is_connection_open():
            self._connection.close()
            self._connection = None
        else:
            raise DataBaseError('Подключение к БД было закрыто')

    def __is_connection_open(self) -> bool:
        return self._connection is not None

    def _execute_query(self, query: str, parameters: tuple = ()) -> list[tuple]:
        cursor = self._connection.cursor()
        try:
            cursor.execute(query, parameters)
        except IntegrityError as e:
            raise ConstraintViolationException(e.args[0])

        return cursor.fetchall()

    def execute_ddl(self, query: str, parameters: tuple = ()) -> None:
        if self.__is_connection_open():
            self._execute_query(query, parameters)
            self._connection.commit()
        else:
            raise DataBaseError('Подключение к БД было закрыто')

    def execute_dml(self, query: str, parameters: tuple = ()) -> list:
        if self.__is_connection_open():
            return self._execute_query(query, parameters)
        else:
            raise DataBaseError('Подключение к БД было закрыто')
