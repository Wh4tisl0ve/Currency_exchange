from src.app.dao.currencies_dao import CurrenciesDAO
from src.app.dao.exchange_rates_dao import ExchangeRatesDAO
from src.app.dto.response.currency_response import CurrencyResponse
from src.app.dto.response.exchange_rates_response import ExchangeRatesResponse
from src.app.dto.response.exchanger_response import ExchangerResponse
from src.app.mappers.exchange_rates_mapper import ExchangeRatesMapper
from src.app.mappers.mapper import Mapper


class ExchangeRatesService:
    def __init__(self, exchange_rates_dao: ExchangeRatesDAO, exchange_rate_mapper: ExchangeRatesMapper):
        self.__exchange_rates_dao = exchange_rates_dao
        self.__exchange_rate_mapper = exchange_rate_mapper

    def get_all_exchange_rates(self) -> list[ExchangeRatesResponse]:
        exchange_rates_data = self.__exchange_rates_dao.get_all_exchange_rates()
        exchange_rates_dto = []
        for ex_rates in exchange_rates_data:
            exchange_rates_dto.append(ExchangeRatesResponse(id=ex_rates[0],
                                                            base_currency=CurrencyResponse(id=ex_rates[1],
                                                                                           name=ex_rates[2],
                                                                                           code=ex_rates[3],
                                                                                           sign=ex_rates[4]),
                                                            target_currency=CurrencyResponse(id=ex_rates[5],
                                                                                             name=ex_rates[6],
                                                                                             code=ex_rates[7],
                                                                                             sign=ex_rates[8]),
                                                            rate=ex_rates[9]))
        return exchange_rates_dto

    def get_exchange_rate(self, base_currency: CurrencyResponse,
                          target_currency: CurrencyResponse) -> ExchangeRatesResponse:
        """base_currency и target_currency будут приходить из контролеера,
        а там будут браться из метода get сервиса валюты"""

        exchange_rate_entity = self.__exchange_rates_dao.get_exchange_rate(base_currency.id, target_currency.id)

        return self.__exchange_rate_mapper.entity_to_dto(exchange_rate_entity, base_currency, target_currency)

    def add_exchange_rate(self, base_currency: CurrencyResponse, target_currency: CurrencyResponse,
                          rate: float) -> ExchangeRatesResponse:
        self.__exchange_rates_dao.add(base_currency.id, target_currency.id, rate)

        exchange_rate_entity = self.__exchange_rates_dao.get_exchange_rate(base_currency.id, target_currency.id)

        return self.__exchange_rate_mapper.entity_to_dto(exchange_rate_entity, base_currency, target_currency)

    def update_exchange_rate(self, base_currency: CurrencyResponse, target_currency: CurrencyResponse,
                             rate: float) -> ExchangeRatesResponse:
        self.__exchange_rates_dao.update(base_currency.id, target_currency.id, rate)

        exchange_rate_entity = self.__exchange_rates_dao.get_exchange_rate(base_currency.id, target_currency.id)

        return self.__exchange_rate_mapper.entity_to_dto(exchange_rate_entity, base_currency, target_currency)
