from src.dao.base_dao import BaseDAO
from src.dto.exchange_rates_dto import ExchangeRatesDTO
from src.database.db_client import DBClient


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

    def get_concrete_exchange_rate(self, base_currency_id: int = 0, target_currency_id: int = 0) -> ExchangeRatesDTO:
        query = f'SELECT * FROM {self._name_entity} WHERE BaseCurrencyID = {base_currency_id} AND TargetCurrencyID = {target_currency_id}'
        self._client_db.open_connection()
        concrete_exchange_rate_fields = self._client_db.execute_dml(query)[0]
        self._client_db.close_connection()

        return ExchangeRatesDTO(id=concrete_exchange_rate_fields[0],
                                base_currency_id=concrete_exchange_rate_fields[1],
                                target_currency_id=concrete_exchange_rate_fields[2],
                                rate=concrete_exchange_rate_fields[3])

    def add(self, base_currency_id: int, target_currency_id: int, rate: float):
        query = f"INSERT INTO {self._name_entity} (BaseCurrencyId, TargetCurrencyId, Rate) VALUES ('{base_currency_id}','{target_currency_id}','{rate}')"
        self._client_db.open_connection()
        self._client_db.execute_ddl(query)
        self._client_db.close_connection()

    def update(self, base_currency_id: int, target_currency_id: int, rate: float):
        query = f"UPDATE {self._name_entity} SET Rate = {rate} WHERE BaseCurrencyId = {base_currency_id} AND TargetCurrencyId = {target_currency_id}"
        self._client_db.open_connection()
        self._client_db.execute_ddl(query)
        self._client_db.close_connection()


