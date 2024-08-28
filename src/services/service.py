from src.dao.currencies_dao import CurrenciesDAO
from src.dao.exchange_rates_dao import ExchangeRatesDAO
from src.dto.currency_dto import CurrencyDTO
from src.dto.exchange_rates_dto import ExchangeRatesDTO


class Service:
    def __init__(self, currencies_dao: CurrenciesDAO, exchange_rate: ExchangeRatesDAO):
        self.__currencies_dao = currencies_dao
        self.__exchange_rates_dao = exchange_rate

    def get_all_currencies(self) -> list[CurrencyDTO]:
        return self.__currencies_dao.get_all_currencies()

    def get_concrete_currency(self, currency_code: str) -> CurrencyDTO:
        return self.__currencies_dao.get_concrete_currency(currency_code)

    def add_currency(self, code: str = '', name: str = '', sign: str = '') -> None:
        self.__currencies_dao.add(code, name, sign)

    def get_all_exchange_rates(self) -> list[ExchangeRatesDTO]:
        return self.__exchange_rates_dao.get_all_exchange_rates()

    def get_concrete_exchange_rate(self, currency_pair: str) -> tuple:
        base_currency_name = currency_pair[:3]
        target_currency_name = currency_pair[3:]

        base_currency = self.__currencies_dao.get_concrete_currency(base_currency_name)
        target_currency = self.__currencies_dao.get_concrete_currency(target_currency_name)

        return self.__exchange_rates_dao.get_concrete_exchange_rates(base_currency.id, target_currency.id)

    def add_exchange_rate(self, base_currency_code: str, target_currency_code: str, rate: float):
        base_currency = self.__currencies_dao.get_concrete_currency(base_currency_code)
        target_currency = self.__currencies_dao.get_concrete_currency(target_currency_code)

        self.__exchange_rates_dao.add(base_currency.id, target_currency.id, rate)







