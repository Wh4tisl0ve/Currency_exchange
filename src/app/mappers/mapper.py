from abc import ABC, abstractmethod


class Mapper(ABC):
    @abstractmethod
    def dto_to_entity(self, dto):
        pass

    @abstractmethod
    def entity_to_dto(self, *args, **kwargs):
        pass
