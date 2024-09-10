from abc import abstractmethod, ABC


class DBClient(ABC):
    @abstractmethod
    def open_connection(self) -> None:
        pass

    @abstractmethod
    def _execute_query(self, query, parameters=()) -> None:
        pass
