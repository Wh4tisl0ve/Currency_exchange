from abc import abstractmethod, ABC

from src.database.db_client import DBClient


class BaseDAO(ABC):
    def __init__(self, db_client: DBClient, name_entity: str):
        self._client_db = db_client
        self._name_entity = name_entity

    def _get_all_entities(self) -> list[tuple]:
        query = f'SELECT * FROM {self._name_entity}'
        self._client_db.open_connection()
        query_result = self._client_db.execute_dml(query)
        self._client_db.close_connection()

        return query_result

    def _get_concrete_entity(self, name_entity: str, find_field: str) -> tuple:
        query = f"SELECT * FROM {self._name_entity} WHERE {find_field} LIKE '{name_entity}'"

        self._client_db.open_connection()
        query_result = self._client_db.execute_dml(query)[0]
        self._client_db.close_connection()

        return query_result

    @abstractmethod
    def add(self, *args):
        pass

    @abstractmethod
    def update(self, *args):
        pass
