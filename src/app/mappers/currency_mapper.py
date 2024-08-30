from src.app.dto.currency_dto import CurrencyDTO
from src.app.entities.currency import Currency
from src.app.mappers.mapper import Mapper


class CurrencyMapper(Mapper):
    def dto_to_entity(self, dto: CurrencyDTO) -> Currency:
        return Currency(id=dto.id, name=dto.name, code=dto.code, sign=dto.sign)

    def entity_to_dto(self, entity: Currency) -> CurrencyDTO:
        return CurrencyDTO(id=entity.id, name=entity.name, code=entity.code, sign=entity.sign)
