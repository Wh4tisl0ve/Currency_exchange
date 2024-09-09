from src.app.exceptions.constraint_violation_error import ConstraintViolationException
from src.app.exceptions.validation_error import ValidationError
from src.app.exceptions.not_found_error import NotFoundError
from src.app.entities.currency import Currency
from src.app.dao.base_dao import BaseDAO


class CurrencyDAO(BaseDAO):
    def __init__(self):
        super().__init__('Currencies')

    def find_all(self) -> list[Currency]:
        currencies = self._find_all_entities()
        currencies_entity = [Currency(id=cur[0], code=cur[1], name=cur[2], sign=cur[3]) for cur in currencies]

        return currencies_entity

    def find_by_code(self, currency_code: str = '') -> Currency:
        try:
            cur_id, cur_code, cur_name, cur_sign = self._find_concrete_entity(currency_code, 'Code')
        except NotFoundError:
            raise NotFoundError(f'Code {currency_code} does not match any currency')

        return Currency(id=cur_id, name=cur_name, code=cur_code, sign=cur_sign)

    def save_entity(self, currency: Currency) -> Currency:
        query = "INSERT INTO Currencies (Code, FullName, Sign) VALUES (?,?,?)"

        try:
            self._client_db.execute_ddl(query, (currency.code, currency.name, currency.sign))
        except ConstraintViolationException as e:
            if 'check' in e.args[0].lower():
                raise ValidationError('The currency code must consist of 3 uppercase Latin letters', 400)
            else:
                raise ConstraintViolationException('The currency with the specified code already exists')

        return self.find_by_code(currency.code)
