from src.app.dao.exchange_rates_dao import ExchangeRatesDAO
from src.app.dto.currency_dto import CurrencyDTO
from src.app.dto.response.exchange_rates_response import ExchangeRatesResponse
from src.app.mappers.exchange_rates_mapper import ExchangeRatesMapper


class ExchangeRatesService:
    def __init__(self, exchange_rates_dao: ExchangeRatesDAO, exchange_rate_mapper: ExchangeRatesMapper):
        self.__exchange_rates_dao = exchange_rates_dao
        self.__exchange_rate_mapper = exchange_rate_mapper

    def get_all_exchange_rates(self) -> list[ExchangeRatesResponse]:
        exchange_rates_data = self.__exchange_rates_dao.get_all_exchange_rates()

        return [self.__exchange_rate_mapper.tuple_to_dto(ex_rates) for ex_rates in exchange_rates_data]

    def get_exchange_rate(self, base_currency: CurrencyDTO,
                          target_currency: CurrencyDTO) -> ExchangeRatesResponse:

        exchange_rate_entity = self.__exchange_rates_dao.get_exchange_rate(base_currency.id, target_currency.id)

        return self.__exchange_rate_mapper.entity_to_dto(exchange_rate_entity, base_currency, target_currency)

    def add_exchange_rate(self, base_currency: CurrencyDTO, target_currency: CurrencyDTO,
                          rate: float) -> ExchangeRatesResponse:
        self.__exchange_rates_dao.add(base_currency.id, target_currency.id, rate)

        exchange_rate_entity = self.__exchange_rates_dao.get_exchange_rate(base_currency.id, target_currency.id)

        return self.__exchange_rate_mapper.entity_to_dto(exchange_rate_entity, base_currency, target_currency)

    def update_exchange_rate(self, base_currency: CurrencyDTO, target_currency: CurrencyDTO,
                             rate: float) -> ExchangeRatesResponse:
        self.__exchange_rates_dao.update(base_currency.id, target_currency.id, rate)

        exchange_rate_entity = self.__exchange_rates_dao.get_exchange_rate(base_currency.id, target_currency.id)

        return self.__exchange_rate_mapper.entity_to_dto(exchange_rate_entity, base_currency, target_currency)
