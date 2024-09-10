from src.app.exceptions.no_content_error import NoContentError
from src.app.exceptions.not_found_error import NotFoundError
from src.app.db_clients.sqlite_client import SQLiteClient
from src.app.db_clients.config.config import load_config
from abc import abstractmethod, ABC


class BaseDAO(ABC):
    def __init__(self, name_entity: str):
        self._client_db = SQLiteClient(load_config())
        self._name_entity = name_entity

    def _find_all_entities(self) -> list[tuple]:
        query = f'SELECT * FROM {self._name_entity}'
        entities = self._client_db.execute_dml(query)
        if not entities:
            raise NoContentError('The query returned an empty data set')

        return entities

    def _find_concrete_entity(self, value_find: str, field_find: str) -> tuple:
        query = f"SELECT * FROM {self._name_entity} WHERE {field_find} LIKE ?"

        try:
            entity = self._client_db.execute_dml(query, (value_find,))[0]
        except IndexError:
            raise NotFoundError('Data not found')

        return entity

    @abstractmethod
    def save_entity(self, *args, **kwargs):
        pass
