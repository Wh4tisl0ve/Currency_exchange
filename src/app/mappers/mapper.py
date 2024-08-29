from abc import ABC, abstractmethod


class Mapper(ABC):
    @abstractmethod
    def dto_to_entity(self, dto: BaseDTO) -> Entity:
        pass

    @abstractmethod
    def entity_to_dto(self, entity: Entity) -> BaseDTO:
        pass
