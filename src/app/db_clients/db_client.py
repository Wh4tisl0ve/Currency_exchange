from src.app.utils.singleton import Singleton
from abc import abstractmethod


class DBClient(metaclass=Singleton):
    def __init__(self):
        self.client = None

    def get_client(self):
        return self.client

    @abstractmethod
    def open_connection(self) -> None:
        pass

    @abstractmethod
    def _execute_query(self, query, parameters=()) -> None:
        pass
