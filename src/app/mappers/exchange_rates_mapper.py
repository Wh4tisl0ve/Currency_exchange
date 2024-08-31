from src.app.dto.request.exchange_rates_req import ExchangeRatesReq
from src.app.dto.request.exchange_rates_request import ExchangeRatesRequest
from src.app.dto.currency_dto import CurrencyDTO
from src.app.dto.response.exchange_rates_response import ExchangeRatesResponse
from src.app.entities.exchange_rate import ExchangeRate
from src.app.mappers.mapper import Mapper


class ExchangeRatesMapper(Mapper):
    def dto_to_entity(self, dto: ExchangeRatesReq) -> ExchangeRate:
        return ExchangeRate(id=0,
                            base_currency_id=dto.base_currency.id,
                            target_currency_id=dto.base_currency.id,
                            rate=dto.rate)

    def entity_to_dto(self, entity: ExchangeRate) -> ExchangeRatesResponse:
        return ExchangeRatesResponse(id=entity.id,
                                     base_currency=base_currency,
                                     target_currency=target_currency,
                                     rate=entity.rate)

    def tuple_to_dto(self, data: tuple) -> ExchangeRatesResponse:
        ex_id, base_id, base_name, base_code, base_sign, target_id, target_name, target_code, target_sign, rate = data

        base_currency = CurrencyDTO(base_id, base_name, base_code, base_sign)
        target_currency = CurrencyDTO(target_id, target_name, target_code, target_sign)

        return ExchangeRatesResponse(ex_id, base_currency, target_currency, rate)
