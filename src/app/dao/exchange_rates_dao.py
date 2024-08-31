from src.app.dao.base_dao import BaseDAO
from src.app.entities.exchange_rate import ExchangeRate
from src.app.database.db_client import DBClient


class ExchangeRatesDAO(BaseDAO):
    def __init__(self, db_client: DBClient):
        super().__init__(db_client, 'ExchangeRates')

    # переработать, чтобы возвращал сущность
    def get_all_exchange_rates(self) -> list[tuple]:
        query = '''SELECT er.id, base.*, target.*, er.rate
                   FROM ExchangeRates er
                   JOIN Currencies as base ON er.BaseCurrencyId = base.id
                   JOIN Currencies as target ON er.TargetCurrencyId = target.id'''

        self._client_db.open_connection()
        list_data_exchange_rates = self._client_db.execute_dml(query)
        self._client_db.close_connection()

        return list_data_exchange_rates

    def get_exchange_rate(self, exchange_rate: ExchangeRate) -> ExchangeRate:
        query = f'''SELECT * FROM {self._name_entity}
                    WHERE BaseCurrencyID = {exchange_rate.base_currency_id}
                    AND TargetCurrencyID = {exchange_rate.target_currency_id}'''

        self._client_db.open_connection()
        er_id, er_base, er_target, er_rate = self._client_db.execute_dml(query)[0]
        self._client_db.close_connection()

        return ExchangeRate(id=er_id, base_currency_id=er_base, target_currency_id=er_target, rate=er_rate)

    def add(self, exchange_rate: ExchangeRate) -> ExchangeRate:
        query = f'''INSERT INTO {self._name_entity} (BaseCurrencyId, TargetCurrencyId, Rate) 
                    VALUES ('{exchange_rate.base_currency_id}',
                            '{exchange_rate.target_currency_id}',
                            '{exchange_rate.rate}')'''

        self._client_db.open_connection()
        self._client_db.execute_ddl(query)
        self._client_db.close_connection()

        return self.get_exchange_rate(exchange_rate)

    def update(self, exchange_rate: ExchangeRate) -> ExchangeRate:
        query = f'''UPDATE {self._name_entity} SET Rate = {exchange_rate.rate} 
                    WHERE BaseCurrencyId = {exchange_rate.base_currency_id} 
                    AND TargetCurrencyId = {exchange_rate.target_currency_id}'''

        self._client_db.open_connection()
        self._client_db.execute_ddl(query)
        self._client_db.close_connection()

        return self.get_exchange_rate(exchange_rate)
