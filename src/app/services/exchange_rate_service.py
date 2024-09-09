from src.app.mappers.exchange_rate_mapper import ExchangeRateMapper
from src.app.dto.exchange_rate_dto import ExchangeRateDTO
from src.app.dao.exchange_rate_dao import ExchangeRateDAO
from src.app.db_clients.db_client import DBClient


class ExchangeRateService:
    def __init__(self, exchange_rates_dao: ExchangeRateDAO):
        self.__exchange_rates_dao = exchange_rates_dao
        self.__exchange_rate_mapper = ExchangeRateMapper()

    def get_all_exchange_rates(self) -> list[ExchangeRateDTO]:
        exchange_rates_data = self.__exchange_rates_dao.find_all()

        return [self.__exchange_rate_mapper.tuple_to_dto(data) for data in exchange_rates_data]

    def get_exchange_rate(self, exchange_rates_request: ExchangeRateDTO) -> ExchangeRateDTO:
        exchange_rate_entity = self.__exchange_rate_mapper.dto_to_entity(exchange_rates_request)
        exchange_rate_entity = self.__exchange_rates_dao.find_by_pair_id(exchange_rate_entity)

        return self.__exchange_rate_mapper.entity_to_dto(exchange_rate_entity)

    def add_exchange_rate(self, exchange_rates_request: ExchangeRateDTO) -> ExchangeRateDTO:
        exchange_rate_entity = self.__exchange_rate_mapper.dto_to_entity(exchange_rates_request)
        exchange_rate_entity = self.__exchange_rates_dao.save_entity(exchange_rate_entity)

        return self.__exchange_rate_mapper.entity_to_dto(exchange_rate_entity)

    def update_exchange_rate(self, exchange_rates_request: ExchangeRateDTO) -> ExchangeRateDTO:
        exchange_rate_entity = self.__exchange_rate_mapper.dto_to_entity(exchange_rates_request)
        exchange_rate_entity = self.__exchange_rates_dao.update(exchange_rate_entity)

        return self.__exchange_rate_mapper.entity_to_dto(exchange_rate_entity)
