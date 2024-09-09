from src.app.dto.exchange_rate_dto import ExchangeRateDTO
from src.app.dto.currency_dto import CurrencyDTO
from src.app.entities.exchange_rate import ExchangeRate
from src.app.mappers.mapper import Mapper


class ExchangeRateMapper(Mapper):
    def dto_to_entity(self, dto: ExchangeRateDTO) -> ExchangeRate:
        return ExchangeRate(id=0,
                            base_currency_id=dto.base_currency.id,
                            target_currency_id=dto.target_currency.id,
                            rate=dto.rate)

    def entity_to_dto(self, entity: ExchangeRate) -> ExchangeRateDTO:
        return ExchangeRateDTO(id=entity.id,
                               base_currency=CurrencyDTO(id=entity.base_currency_id),
                               target_currency=CurrencyDTO(id=entity.target_currency_id),
                               rate=entity.rate)

    def tuple_to_dto(self, data: tuple) -> ExchangeRateDTO:
        ex_id, base_id, base_code, base_name, base_sign, target_id, target_code, target_name, target_sign, rate = data
        base_currency = CurrencyDTO(base_id, base_name, base_code, base_sign)
        target_currency = CurrencyDTO(target_id, target_name, target_code, target_sign)

        return ExchangeRateDTO(base_currency=base_currency,
                               target_currency=target_currency,
                               id=ex_id,
                               rate=rate)
