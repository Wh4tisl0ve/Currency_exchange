from src.app.exceptions.constraint_violation_error import ConstraintViolationException
from src.app.exceptions.not_found_error import NotFoundError
from src.app.entities.exchange_rate import ExchangeRate
from src.app.dao.base_dao import BaseDAO
from decimal import Decimal


class ExchangeRateDAO(BaseDAO):
    def __init__(self):
        super().__init__('ExchangeRates')

    def find_all(self) -> list[tuple]:
        query = '''SELECT er.id, base.*, target.*, er.rate
                   FROM ExchangeRates er
                   JOIN Currencies as base ON er.BaseCurrencyId = base.id
                   JOIN Currencies as target ON er.TargetCurrencyId = target.id'''

        exchange_rates_data = self._client_db.execute_dml(query)

        return exchange_rates_data

    def find_by_pair_id(self, exchange_rate: ExchangeRate) -> ExchangeRate:
        query = f'SELECT * FROM {self._name_entity} WHERE BaseCurrencyID = ? AND TargetCurrencyID = ?'

        try:
            data = (exchange_rate.base_currency_id, exchange_rate.target_currency_id)
            er_id, er_base, er_target, er_rate = self._client_db.execute_dml(query, data)[0]
        except IndexError:
            raise NotFoundError('Exchange rate for currency pair not found')

        return ExchangeRate(id=er_id, base_currency_id=er_base, target_currency_id=er_target, rate=Decimal(er_rate))

    def save_entity(self, exchange_rate: ExchangeRate) -> ExchangeRate:
        query = f'INSERT INTO {self._name_entity} (BaseCurrencyId, TargetCurrencyId, Rate) VALUES (?,?,?)'

        try:
            self._client_db.execute_ddl(query, (exchange_rate.base_currency_id,
                                                exchange_rate.target_currency_id,
                                                float(exchange_rate.rate)))
        except ConstraintViolationException as e:
            if 'check' in e.args[0].lower():
                message = 'Cannot add a rate with the same base and target currency code'
            else:
                message = 'A currency pair with this code already exists'
            raise ConstraintViolationException(message)

        return self.find_by_pair_id(exchange_rate)

    def update(self, exchange_rate: ExchangeRate) -> ExchangeRate:
        query = f'UPDATE {self._name_entity} SET Rate = ? WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?'

        self._client_db.execute_ddl(query, (float(exchange_rate.rate),
                                            exchange_rate.base_currency_id,
                                            exchange_rate.target_currency_id))

        return self.find_by_pair_id(exchange_rate)
