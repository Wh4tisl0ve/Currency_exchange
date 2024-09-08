from src.app.exceptions.db_error.database_error import DataBaseError
from src.app.exceptions.no_content_error import NoContentError
from src.app.exceptions.not_found_error import NotFoundError
from src.app.db_clients.db_client import DBClient
from sqlite3 import OperationalError
from abc import abstractmethod, ABC


class BaseDAO(ABC):
    def __init__(self, db_client: DBClient, name_entity: str):
        self._client_db = db_client
        self._name_entity = name_entity

    def _get_all_entities(self) -> list[tuple]:
        query = f'SELECT * FROM {self._name_entity}'
        self._client_db.open_connection()
        try:
            entities = self._client_db.execute_dml(query)
            if not entities:
                raise NoContentError('Запрос вернул пустой набор данных')
        except OperationalError:
            raise DataBaseError('Невозможно получить данные')
        self._client_db.close_connection()

        return entities

    def _get_concrete_entity(self, value_find: str, field_find: str) -> tuple:
        query = f"SELECT * FROM {self._name_entity} WHERE {field_find} LIKE '{value_find}'"

        self._client_db.open_connection()
        try:
            entity = self._client_db.execute_dml(query)[0]
        except IndexError:
            raise NotFoundError('Данные не найдены')
        self._client_db.close_connection()

        return entity

    @abstractmethod
    def add(self, *args, **kwargs):
        pass
