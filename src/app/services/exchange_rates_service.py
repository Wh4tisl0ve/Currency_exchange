from src.app.mappers.exchange_rates_mapper import ExchangeRatesMapper
from src.app.dto.exchange_rates_dto import ExchangeRatesDTO
from src.app.dao.exchange_rates_dao import ExchangeRatesDAO
from src.app.database.db_client import DBClient


class ExchangeRatesService:
    def __init__(self, db_client: DBClient):
        self.__exchange_rates_dao = ExchangeRatesDAO(db_client)
        self.__exchange_rate_mapper = ExchangeRatesMapper()

    def get_all_exchange_rates(self) -> list[ExchangeRatesDTO]:
        exchange_rates_data = self.__exchange_rates_dao.get_all_exchange_rates()

        return [self.__exchange_rate_mapper.tuple_to_dto(data) for data in exchange_rates_data]

    def get_exchange_rate(self, exchange_rates_request: ExchangeRatesDTO) -> ExchangeRatesDTO:
        exchange_rate_entity = self.__exchange_rate_mapper.dto_to_entity(exchange_rates_request)
        exchange_rate_entity = self.__exchange_rates_dao.get_exchange_rate(exchange_rate_entity)

        return self.__exchange_rate_mapper.entity_to_dto(exchange_rate_entity)

    def add_exchange_rate(self, exchange_rates_request: ExchangeRatesDTO) -> ExchangeRatesDTO:
        exchange_rate_entity = self.__exchange_rate_mapper.dto_to_entity(exchange_rates_request)
        exchange_rate_entity = self.__exchange_rates_dao.add(exchange_rate_entity)

        return self.__exchange_rate_mapper.entity_to_dto(exchange_rate_entity)

    def update_exchange_rate(self, exchange_rates_request: ExchangeRatesDTO) -> ExchangeRatesDTO:
        exchange_rate_entity = self.__exchange_rate_mapper.dto_to_entity(exchange_rates_request)
        exchange_rate_entity = self.__exchange_rates_dao.update(exchange_rate_entity)

        return self.__exchange_rate_mapper.entity_to_dto(exchange_rate_entity)
