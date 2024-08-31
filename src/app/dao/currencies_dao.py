from src.app.dao.base_dao import BaseDAO
from src.app.entities.currency import Currency
from src.app.database.db_client import DBClient


class CurrenciesDAO(BaseDAO):
    def __init__(self, db_client: DBClient):
        super().__init__(db_client, 'Currencies')

    def get_all_currencies(self) -> list[Currency]:
        list_all_currencies = self._get_all_entities()
        all_currencies = [Currency(id=cur[0], name=cur[1], code=cur[2], sign=cur[3]) for cur in list_all_currencies]

        return all_currencies

    def get_currency_by_code(self, currency_code: str = '') -> Currency:
        cur_id, cur_name, cur_code, cur_sign = self._get_concrete_entity(currency_code, 'Code')

        return Currency(id=cur_id, name=cur_name, code=cur_code, sign=cur_sign)

    def get_currency_by_id(self, currency_id: int) -> Currency:
        cur_id, cur_name, cur_code, cur_sign = self._get_concrete_entity(str(currency_id), 'ID')

        return Currency(id=cur_id, name=cur_name, code=cur_code, sign=cur_sign)

    def add(self, currency: Currency) -> Currency:
        query = f'''INSERT INTO Currencies (Code, FullName, Sign) 
                    VALUES ('{currency.code}','{currency.name}','{currency.sign}')'''

        self._client_db.open_connection()
        self._client_db.execute_ddl(query)
        self._client_db.close_connection()

        return self.get_currency_by_code(currency.code)
