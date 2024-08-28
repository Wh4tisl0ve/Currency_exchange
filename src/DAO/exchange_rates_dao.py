from src.DAO.base_dao import BaseDAO
from src.DTO.exchange_rates_dto import ExchangeRatesDTO
from src.Database.db_client import DBClient


class ExchangeRatesDAO(BaseDAO):
    def __init__(self, db_client: DBClient):
        super().__init__(db_client, 'ExchangeRates')

    def get_all_exchange_rates(self) -> list[ExchangeRatesDTO]:
        list_all_exchange_rates = self._get_all_entities()

        all_exchange_rates = [ExchangeRatesDTO(id=ex_rate[0],
                                               base_currency_id=ex_rate[1],
                                               target_currency_id=ex_rate[2],
                                               rate=ex_rate[3])
                              for ex_rate in list_all_exchange_rates]

        return all_exchange_rates

    def get_concrete_exchange_rates(self, base_currency_id: int, target_currency_id: int) -> tuple:
        print(base_currency_id)
        print(target_currency_id)