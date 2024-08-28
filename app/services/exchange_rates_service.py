from app.dao.currencies_dao import CurrenciesDAO
from app.dao.exchange_rates_dao import ExchangeRatesDAO
from app.dto.exchange_rates_dto import ExchangeRatesDTO


class ExchangeRatesService:
    def __init__(self, exchange_rates_dao: ExchangeRatesDAO, currencies_dao: CurrenciesDAO):
        self.__exchange_rates_dao = exchange_rates_dao
        self.__currencies_dao = currencies_dao

    def get_all_exchange_rates(self) -> list[ExchangeRatesDTO]:
        return self.__exchange_rates_dao.get_all_exchange_rates()

    def get_concrete_exchange_rate(self, currency_pair: str) -> ExchangeRatesDTO:
        base_currency_code, target_currency_code = currency_pair[:3], currency_pair[3:]

        base_currency = self.__currencies_dao.get_currency(base_currency_code)
        target_currency = self.__currencies_dao.get_currency(target_currency_code)

        return self.__exchange_rates_dao.get_exchange_rate(base_currency.id, target_currency.id)

    def add_exchange_rate(self, base_currency_code: str, target_currency_code: str, rate: float) -> None:
        base_currency = self.__currencies_dao.get_currency(base_currency_code)
        target_currency = self.__currencies_dao.get_currency(target_currency_code)

        self.__exchange_rates_dao.add(base_currency.id, target_currency.id, rate)

    def update_exchange_rate(self, currency_pair: str, rate: float) -> None:
        base_currency_code, target_currency_code = currency_pair[:3], currency_pair[3:]

        base_currency = self.__currencies_dao.get_currency(base_currency_code)
        target_currency = self.__currencies_dao.get_currency(target_currency_code)

        self.__exchange_rates_dao.update(base_currency.id, target_currency.id, rate)

    def perform_currency_exchange(self, base_currency_code: str, target_currency_code: str, amount: float):
        base_currency = self.__currencies_dao.get_currency(base_currency_code)
        target_currency = self.__currencies_dao.get_currency(target_currency_code)

        direct_exchange_rate = self.__exchange_rates_dao.get_exchange_rate(base_currency.id, target_currency.id)
        reverse_exchange_rate = self.__exchange_rates_dao.get_exchange_rate(target_currency.id, base_currency.id)

        if direct_exchange_rate is not None:
            converted_amount = direct_exchange_rate.rate * amount
        elif reverse_exchange_rate is not None:
            converted_amount = amount / reverse_exchange_rate.rate
        else:
            converted_amount = self.exchange_via_usd(base_currency, target_currency, amount)

    def exchange_via_usd(self, base_currency: CurrenciesDAO, target_currency: CurrenciesDAO, amount: float) -> float:
        usd_currency = self.__currencies_dao.get_currency('USD')
        base_usd_exchange_rate = self.__exchange_rates_dao.get_exchange_rate(base_currency.id, usd_currency.id)
        target_usd_exchange_rate = self.__exchange_rates_dao.get_exchange_rate(usd_currency.id, target_currency.id)

        converted_amount = (amount * base_usd_exchange_rate.rate) * target_usd_exchange_rate.rate
        return converted_amount