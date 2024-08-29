from src.app.dao.currencies_dao import CurrenciesDAO
from src.app.dao.exchange_rates_dao import ExchangeRatesDAO
from src.app.dto.response.currency_response import CurrencyResponse
from src.app.dto.response.exchange_rates_response import ExchangeRatesResponse
from src.app.mappers.exchange_rates_mapper import ExchangeRatesMapper
from src.app.mappers.mapper import Mapper


class ExchangeRatesService:
    def __init__(self, exchange_rates_dao: ExchangeRatesDAO, currencies_dao: CurrenciesDAO, exchange_rate_mapper: ExchangeRatesMapper):
        self.__exchange_rates_dao = exchange_rates_dao
        self.__currencies_dao = currencies_dao
        self.__exchange_rate_mapper = exchange_rate_mapper

    def get_all_exchange_rates(self) -> list[ExchangeRatesResponse]:
        exchange_rates_entity = self.__exchange_rates_dao.get_all_exchange_rates()
        exchange_rates_dto = []

        for exchange_rate in exchange_rates_entity:
            base_currency_entity = self.__currencies_dao.get_currency_by_id(exchange_rate.base_currency_id)
            target_currency_entity = self.__currencies_dao.get_currency_by_id(exchange_rate.target_currency_id)

            # как получить response?

            self.__exchange_rate_mapper.entity_to_dto(exchange_rate, base_currency, target_currency)
            exchange_rates_dto.append()

        return None

    def get_concrete_exchange_rate(self, currency_pair: str) -> ExchangeRatesResponse:
        base_currency_code, target_currency_code = currency_pair[:3], currency_pair[3:]

        base_currency = self.__currencies_dao.get_currency_by_code(base_currency_code)
        target_currency = self.__currencies_dao.get_currency_by_code(target_currency_code)

        return self.__exchange_rates_dao.get_exchange_rate(base_currency.id, target_currency.id)

    def add_exchange_rate(self, base_currency_code: str, target_currency_code: str, rate: float) -> None:
        base_currency = self.__currencies_dao.get_currency_by_code(base_currency_code)
        target_currency = self.__currencies_dao.get_currency_by_code(target_currency_code)

        self.__exchange_rates_dao.add(base_currency.id, target_currency.id, rate)

    def update_exchange_rate(self, currency_pair: str, rate: float) -> None:
        base_currency_code, target_currency_code = currency_pair[:3], currency_pair[3:]

        base_currency = self.__currencies_dao.get_currency_by_code(base_currency_code)
        target_currency = self.__currencies_dao.get_currency_by_code(target_currency_code)

        self.__exchange_rates_dao.update(base_currency.id, target_currency.id, rate)

    def perform_currency_exchange(self, base_currency_code: str, target_currency_code: str, amount: float):
        base_currency = self.__currencies_dao.get_currency_by_code(base_currency_code)
        target_currency = self.__currencies_dao.get_currency_by_code(target_currency_code)

        direct_exchange_rate = self.__exchange_rates_dao.get_exchange_rate(base_currency.id, target_currency.id)
        reverse_exchange_rate = self.__exchange_rates_dao.get_exchange_rate(target_currency.id, base_currency.id)

        if direct_exchange_rate is not None:
            converted_amount = direct_exchange_rate.rate * amount
        elif reverse_exchange_rate is not None:
            converted_amount = amount / reverse_exchange_rate.rate
        else:
            converted_amount = self.exchange_via_usd(base_currency, target_currency, amount)

        return converted_amount

    def exchange_via_usd(self, base_currency: CurrencyResponse, target_currency: CurrencyResponse,
                         amount: float) -> float:
        usd_currency = self.__currencies_dao.get_currency_by_code('USD')
        base_usd_exchange_rate = self.__exchange_rates_dao.get_exchange_rate(base_currency.id, usd_currency.id)
        target_usd_exchange_rate = self.__exchange_rates_dao.get_exchange_rate(usd_currency.id, target_currency.id)

        converted_amount = (amount * base_usd_exchange_rate.rate) * target_usd_exchange_rate.rate
        return converted_amount
