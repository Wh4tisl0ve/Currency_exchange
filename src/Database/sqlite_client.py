import sqlite3
from sqlite3 import DatabaseError
from src.Database.db_client import DBClient


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
            raise DatabaseError('Подключение к БД было закрыто')

    def __is_connection_open(self) -> bool:
        return self._connection is not None

    def execute(self, query, parameters=()) -> None:
        if self.__is_connection_open():
            cursor = self._connection.cursor()
            cursor.execute(query, parameters)
            self._connection.commit()
        else:
            raise DatabaseError('Подключение к БД было закрыто')
