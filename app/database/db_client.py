from abc import ABC, abstractmethod


class DBClient(ABC):
    def __init__(self, config: dict):
        self._config = config
        self._connection = None

    @abstractmethod
    def open_connection(self) -> None:
        pass

    @abstractmethod
    def close_connection(self) -> None:
        pass

    @abstractmethod
    def _execute(self, query, parameters=()) -> None:
        pass
