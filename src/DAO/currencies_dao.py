from src.DAO.base_dao import BaseDAO
from src.DTO.currency_dto import CurrencyDTO
from src.Database.db_client import DBClient


class CurrenciesDAO(BaseDAO):
    def __init__(self, db_client: DBClient):
        super().__init__(db_client, 'Currencies')

    def get_all_currencies(self) -> list[CurrencyDTO]:
        list_all_currencies = self._get_all_entities()
        all_currencies = [CurrencyDTO(id=cur[0],
                                      name=cur[1],
                                      code=cur[2],
                                      sign=cur[3]) for cur in list_all_currencies]

        return all_currencies

    def get_concrete_currency(self, currency_code: str) -> CurrencyDTO:
        concrete_currency = self._get_concrete_entity(currency_code, 'Code')

        return CurrencyDTO(id=concrete_currency[0],
                           name=concrete_currency[1],
                           code=concrete_currency[2],
                           sign=concrete_currency[3])

    def add(self, code: str = '', name: str = '', sign: str = '') -> None:
        query = f"INSERT INTO Currencies (Code, FullName, Sign) VALUES ('{code}','{name}','{sign}')"
        self.__client_db.open_connection()
        self.__client_db.execute_ddl(query)
        self.__client_db.close_connection()
        print(f"{code},{name},{sign}")
