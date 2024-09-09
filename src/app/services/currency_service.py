from src.app.mappers.currency_mapper import CurrencyMapper
from src.app.dao.currency_dao import CurrencyDAO
from src.app.dto.currency_dto import CurrencyDTO


class CurrencyService:
    def __init__(self):
        self.__currencies_dao = CurrencyDAO()
        self.__currency_mapper = CurrencyMapper()

    def get_all_currencies(self) -> list[CurrencyDTO]:
        currencies = self.__currencies_dao.find_all()

        return [self.__currency_mapper.entity_to_dto(currency) for currency in currencies]

    def get_concrete_currency(self, currency_code: str) -> CurrencyDTO:
        concrete_currency = self.__currencies_dao.find_by_code(currency_code)

        return self.__currency_mapper.entity_to_dto(concrete_currency)

    def add_currency(self, currency_request: CurrencyDTO) -> CurrencyDTO:
        currency_entity = self.__currency_mapper.dto_to_entity(currency_request)
        currency_entity = self.__currencies_dao.save_entity(currency_entity)

        return self.__currency_mapper.entity_to_dto(currency_entity)
