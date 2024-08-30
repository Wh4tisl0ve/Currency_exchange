from src.app.dto.request.exchange_rates_request import ExchangeRatesRequest
from src.app.dto.response.currency_response import CurrencyResponse
from src.app.dto.response.exchange_rates_response import ExchangeRatesResponse
from src.app.entities.exchange_rate import ExchangeRate
from src.app.mappers.mapper import Mapper


class ExchangeRatesMapper(Mapper):
    def dto_to_entity(self, dto: ExchangeRatesRequest) -> ExchangeRate:
        return ExchangeRate(id=0, name=dto.b, code=dto.code, sign=dto.sign)

    def entity_to_dto(self, entity: ExchangeRate, base_currency: CurrencyResponse, target_currency: CurrencyResponse) -> ExchangeRatesResponse:
        return ExchangeRatesResponse(id=entity.id,
                                     base_currency=base_currency,
                                     target_currency=target_currency,
                                     rate=entity.rate)
