from src.app.dao.currencies_dao import CurrenciesDAO
from src.app.dto.currency_dto import CurrencyDTO
from src.app.mappers.currency_mapper import CurrencyMapper


class CurrencyService:
    def __init__(self, currencies_dao: CurrenciesDAO, currency_mapper: CurrencyMapper):
        self.__currencies_dao = currencies_dao
        self.__currency_mapper = currency_mapper

    def get_all_currencies(self) -> list[CurrencyDTO]:
        currencies = self.__currencies_dao.get_all_currencies()

        return [self.__currency_mapper.entity_to_dto(currency) for currency in currencies]

    def get_concrete_currency(self, currency_code: str) -> CurrencyDTO:
        concrete_currency = self.__currencies_dao.get_currency_by_code(currency_code)

        return self.__currency_mapper.entity_to_dto(concrete_currency)

    def add_currency(self, currency_request: CurrencyDTO) -> CurrencyDTO:
        currency_entity = self.__currency_mapper.dto_to_entity(currency_request)
        currency_entity = self.__currencies_dao.add(currency_entity)

        return self.__currency_mapper.entity_to_dto(currency_entity)
