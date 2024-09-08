from src.app.dto.exchange_rates_dto import ExchangeRatesDTO
from src.app.dto.currency_dto import CurrencyDTO
from src.app.entities.exchange_rate import ExchangeRate
from src.app.mappers.mapper import Mapper


class ExchangeRatesMapper(Mapper):
    def dto_to_entity(self, dto: ExchangeRatesDTO) -> ExchangeRate:
        return ExchangeRate(id=0,
                            base_currency_id=dto.base_currency.id,
                            target_currency_id=dto.target_currency.id,
                            rate=dto.rate)

    def entity_to_dto(self, entity: ExchangeRate) -> ExchangeRatesDTO:
        return ExchangeRatesDTO(id=entity.id,
                                base_currency=CurrencyDTO(id=entity.base_currency_id),
                                target_currency=CurrencyDTO(id=entity.target_currency_id),
                                rate=entity.rate)

    def tuple_to_dto(self, data: tuple) -> ExchangeRatesDTO:
        ex_id, base_id, base_code, base_name, base_sign, target_id, target_code, target_name, target_sign, rate = data
        print(data)
        base_currency = CurrencyDTO(base_id, base_name, base_code, base_sign)
        target_currency = CurrencyDTO(target_id, target_name, target_code, target_sign)

        return ExchangeRatesDTO(base_currency=base_currency,
                                target_currency=target_currency,
                                id=ex_id,
                                rate=rate)
