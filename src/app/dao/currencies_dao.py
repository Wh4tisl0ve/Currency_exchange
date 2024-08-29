from src.app.dao.base_dao import BaseDAO
from src.app.entities.currency import Currency
from src.app.database.db_client import DBClient


class CurrenciesDAO(BaseDAO):
    def __init__(self, db_client: DBClient):
        super().__init__(db_client, 'Currencies')

    def get_all_currencies(self) -> list[Currency]:
        list_all_currencies = self._get_all_entities()
        all_currencies = [Currency(id=cur[0],
                                   name=cur[1],
                                   code=cur[2],
                                   sign=cur[3]) for cur in list_all_currencies]

        return all_currencies

    def get_currency(self, currency_code: str = '') -> Currency:
        concrete_currency = self._get_concrete_entity(currency_code, 'Code')

        return Currency(id=concrete_currency[0],
                        name=concrete_currency[1],
                        code=concrete_currency[2],
                        sign=concrete_currency[3])

    def add(self, code: str = '', name: str = '', sign: str = '') -> None:
        query = f"INSERT INTO Currencies (Code, FullName, Sign) VALUES ('{code}','{name}','{sign}')"
        self._client_db.open_connection()
        self._client_db.execute_ddl(query)
        self._client_db.close_connection()
