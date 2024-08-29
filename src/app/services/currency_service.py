from src.app.dao.currencies_dao import CurrenciesDAO
from src.app.dto.request.currency_request import CurrencyRequest
from src.app.dto.response.currency_response import CurrencyResponse
from src.app.mappers.currency_mapper import CurrencyMapper


class CurrencyService:
    def __init__(self, currencies_dao: CurrenciesDAO, currency_mapper: CurrencyMapper):
        self.__currencies_dao = currencies_dao
        self.__currency_mapper = currency_mapper

    def get_all_currencies(self) -> list[CurrencyResponse]:
        currencies = self.__currencies_dao.get_all_currencies()

        return [self.__currency_mapper.entity_to_dto(currency) for currency in currencies]

    def get_concrete_currency(self, currency_code: str) -> CurrencyResponse:
        concrete_currency = self.__currencies_dao.get_currency_by_code(currency_code)

        return self.__currency_mapper.entity_to_dto(concrete_currency)

    def add_currency(self, code: str = '', name: str = '', sign: str = '') -> CurrencyResponse:
        currency_request = CurrencyRequest(code=code, name=name, sign=sign)
        self.__currencies_dao.add(currency_request)
        added_currency = self.get_concrete_currency(code)
        return added_currency
