from src.DAO.currencies_dao import CurrenciesDAO
from src.DAO.exchange_rates_dao import ExchangeRatesDAO


class Service:
    def __init__(self, currencies_dao: CurrenciesDAO, exchange_rate: ExchangeRatesDAO):
        self.__currencies_dao = currencies_dao
        self.__exchange_rates_dao = exchange_rate

    def get_concrete_exchange_rate(self, currency_pair: str):
        base_currency_name = currency_pair[:3]
        target_currency_name = currency_pair[3:]

        base_currency = self.__currencies_dao.get_concrete_currency(base_currency_name)
        target_currency = self.__currencies_dao.get_concrete_currency(target_currency_name)

        self.__exchange_rates_dao.get_concrete_exchange_rates(base_currency.id, target_currency.id)





