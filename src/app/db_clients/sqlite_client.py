from src.app.exceptions.constraint_violation_error import ConstraintViolationException
from src.app.exceptions.db_error.database_error import DataBaseError
from src.app.exceptions.not_found_error import NotFoundError
from src.app.db_clients.db_client import DBClient
from sqlite3 import IntegrityError, OperationalError, DatabaseError, Connection
import sqlite3
import os


class SQLiteClient(DBClient):
    def __init__(self, config_db: dict):
        self.__config = config_db

    def open_connection(self) -> Connection:
        return self._create_connection()

    def _create_connection(self) -> Connection:
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            resources_dir = os.path.join(current_dir, '..', self.__config['sqlite']['database_path'])
            return sqlite3.connect(resources_dir)
        except OperationalError:
            raise NotFoundError('The database file was not found')
        except DatabaseError:
            raise DataBaseError('The database is unavailable')

    def _execute_query(self, query: str, parameters: tuple = ()) -> list[tuple]:
        cursor = self.__connection.cursor()
        try:
            cursor.execute(query, parameters)
            data = cursor.fetchall()
            cursor.close()
        except IntegrityError as e:
            raise ConstraintViolationException(e.args[0])
        except OperationalError:
            raise DataBaseError('The data source is missing')

        return data

    def execute_ddl(self, query: str, parameters: tuple = ()) -> None:
        with self:
            self._execute_query(query, parameters)
            self.__connection.commit()

    def execute_dml(self, query: str, parameters: tuple = ()) -> list:
        with self:
            return self._execute_query(query, parameters)

    def __enter__(self):
        self.__connection = self._create_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__connection:
            self.__connection.close()
            self.__connection = None
