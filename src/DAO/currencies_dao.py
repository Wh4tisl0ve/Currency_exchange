from src.DTO.currency_dto import CurrencyDTO
from src.Database.db_client import DBClient


class CurrenciesDAO:
    def __init__(self, db_client: DBClient):
        self.__client_db = db_client

    def get_all_currencies(self) -> list[CurrencyDTO]:
        query = 'SELECT * FROM Currencies'
        self.__client_db.open_connection()
        list_query_result = self.__client_db.execute_dml(query)
        self.__client_db.close_connection()
        list_all_currencies = []

        return list_all_currencies

    def get_concrete_currency(self, currency_code: str) -> CurrencyDTO:
        query = f"SELECT * FROM Currencies WHERE Code = '{currency_code}'"

        self.__client_db.open_connection()
        currency = self.__client_db.execute_dml(query)[0]
        self.__client_db.close_connection()

        return CurrencyDTO(id=currency[0],name=currency[1],code=currency[2], sign=currency[3])

    def add(self, name: str, code: str, sign: str):
        pass
