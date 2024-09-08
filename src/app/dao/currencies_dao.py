from src.app.exceptions.currency_error.currency_not_found_error import CurrencyNotFoundError
from src.app.exceptions.constraint_violation_error import ConstraintViolationException
from src.app.exceptions.currency_error.currency_already_exists_error import CurrencyAlreadyExists
from src.app.exceptions.not_found_error import NotFoundError
from src.app.database.db_client import DBClient
from src.app.entities.currency import Currency
from src.app.dao.base_dao import BaseDAO


class CurrenciesDAO(BaseDAO):
    def __init__(self, db_client: DBClient):
        super().__init__(db_client, 'Currencies')

    def get_all_currencies(self) -> list[Currency]:
        currencies = self._get_all_entities()
        currencies_entity = [Currency(id=cur[0], name=cur[1], code=cur[2], sign=cur[3]) for cur in currencies]

        return currencies_entity

    def get_currency_by_code(self, currency_code: str = '') -> Currency:
        try:
            cur_id, cur_name, cur_code, cur_sign = self._get_concrete_entity(currency_code, 'Code')
        except NotFoundError:
            raise CurrencyNotFoundError(f'Код {currency_code} не соответствует ни одной валюте')

        return Currency(id=cur_id, name=cur_name, code=cur_code, sign=cur_sign)

    def add(self, currency: Currency) -> Currency:
        query = "INSERT INTO Currencies (Code, FullName, Sign) VALUES (?,?,?)"

        self._client_db.open_connection()
        try:
            self._client_db.execute_ddl(query, (currency.code, currency.name, currency.sign))
        except ConstraintViolationException:
            raise CurrencyAlreadyExists('Валюта с указанным кодом уже существует')
        self._client_db.close_connection()

        return self.get_currency_by_code(currency.code)
