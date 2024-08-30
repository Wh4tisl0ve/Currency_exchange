from src.app.dao.base_dao import BaseDAO
from src.app.entities.exchange_rate import ExchangeRate
from src.app.database.db_client import DBClient


class ExchangeRatesDAO(BaseDAO):
    def __init__(self, db_client: DBClient):
        super().__init__(db_client, 'ExchangeRates')

    def get_all_exchange_rates(self) -> list[tuple]:
        query = '''SELECT er.id, base.*, target.*, er.rate
                   FROM ExchangeRates er
                   JOIN Currencies as base ON er.BaseCurrencyId = base.id
                   JOIN Currencies as target ON er.TargetCurrencyId = target.id
                                        '''

        self._client_db.open_connection()
        list_all_exchange_rates = self._client_db.execute_dml(query)
        self._client_db.close_connection()

        return list_all_exchange_rates

    def get_exchange_rate(self, base_currency_id: int, target_currency_id: int) -> ExchangeRate:
        query = f'SELECT * FROM {self._name_entity} WHERE BaseCurrencyID = {base_currency_id} AND TargetCurrencyID = {target_currency_id}'
        self._client_db.open_connection()
        concrete_exchange_rate_fields = self._client_db.execute_dml(query)[0]
        self._client_db.close_connection()

        return ExchangeRate(id=concrete_exchange_rate_fields[0],
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


