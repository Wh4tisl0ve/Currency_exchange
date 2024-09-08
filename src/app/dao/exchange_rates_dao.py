from src.app.exceptions.exchange_rates_error.exchange_rates_not_found_error import ExchangeRateNotFoundError
from src.app.exceptions.exchange_rates_error.exchange_rate_already_exists import ExchangeRateAlreadyExists
from src.app.exceptions.constraint_violation_exception import ConstraintViolationException
from src.app.entities.exchange_rate import ExchangeRate
from src.app.database.db_client import DBClient
from src.app.dao.base_dao import BaseDAO
from decimal import Decimal


class ExchangeRatesDAO(BaseDAO):
    def __init__(self, db_client: DBClient):
        super().__init__(db_client, 'ExchangeRates')

    def get_all_exchange_rates(self) -> list[tuple]:
        query = '''SELECT er.id, base.*, target.*, er.rate
                   FROM ExchangeRates er
                   JOIN Currencies as base ON er.BaseCurrencyId = base.id
                   JOIN Currencies as target ON er.TargetCurrencyId = target.id'''

        self._client_db.open_connection()
        exchange_rates_data = self._client_db.execute_dml(query)
        self._client_db.close_connection()

        return exchange_rates_data

    def get_exchange_rate(self, exchange_rate: ExchangeRate) -> ExchangeRate:
        query = f'SELECT * FROM {self._name_entity} WHERE BaseCurrencyID = ? AND TargetCurrencyID = ?'

        self._client_db.open_connection()
        try:
            data = (exchange_rate.base_currency_id, exchange_rate.target_currency_id)
            er_id, er_base, er_target, er_rate = self._client_db.execute_dml(query, data)[0]
        except IndexError:
            raise ExchangeRateNotFoundError('Обменный курс для пары не найден')
        self._client_db.close_connection()

        return ExchangeRate(id=er_id, base_currency_id=er_base, target_currency_id=er_target, rate=Decimal(er_rate))

    def add(self, exchange_rate: ExchangeRate) -> ExchangeRate:
        query = f'INSERT INTO {self._name_entity} (BaseCurrencyId, TargetCurrencyId, Rate) VALUES (?,?,?)'

        self._client_db.open_connection()
        try:
            self._client_db.execute_ddl(query, (exchange_rate.base_currency_id,
                                                exchange_rate.target_currency_id,
                                                exchange_rate.rate))
        except ConstraintViolationException:
            raise ExchangeRateAlreadyExists('Валютная пара с таким кодом уже существует')
        self._client_db.close_connection()

        return self.get_exchange_rate(exchange_rate)

    def update(self, exchange_rate: ExchangeRate) -> ExchangeRate:
        query = f'UPDATE {self._name_entity} SET Rate = ? WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?'

        self._client_db.open_connection()
        self._client_db.execute_ddl(query, (exchange_rate.rate,
                                            exchange_rate.base_currency_id,
                                            exchange_rate.target_currency_id))
        self._client_db.close_connection()

        return self.get_exchange_rate(exchange_rate)
