from app.dao.currencies_dao import CurrenciesDAO
from app.dto.currency_dto import CurrencyDTO


class CurrencyService:
    def __init__(self, currencies_dao: CurrenciesDAO):
        self.__currencies_dao = currencies_dao

    def get_all_currencies(self) -> list[CurrencyDTO]:
        return self.__currencies_dao.get_all_currencies()

    def get_concrete_currency(self, currency_code: str) -> CurrencyDTO:
        return self.__currencies_dao.get_currency(currency_code)

    def add_currency(self, code: str = '', name: str = '', sign: str = '') -> None:
        self.__currencies_dao.add(code, name, sign)
