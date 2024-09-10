from abc import abstractmethod, ABC


class DBClient(ABC):
    @abstractmethod
    def _create_connection(self):
        pass

    @abstractmethod
    def open_connection(self) -> None:
        pass

    @abstractmethod
    def _execute_query(self, query, parameters=()) -> None:
        pass
