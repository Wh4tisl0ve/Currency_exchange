from src.app.dto.request.currency_request import CurrencyRequest
from src.app.dto.response.currency_response import CurrencyResponse
from src.app.entities.currency import Currency
from src.app.mappers.mapper import Mapper


class CurrencyMapper(Mapper):
    def dto_to_entity(self, dto: CurrencyRequest) -> Currency:
        return Currency(id=0, name=dto.name, code=dto.code, sign=dto.sign)

    def entity_to_dto(self, entity: Currency) -> CurrencyResponse:
        return CurrencyResponse(id=entity.id, name=entity.name, code=entity.code, sign=entity.sign)
