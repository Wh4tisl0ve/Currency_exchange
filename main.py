import json

from src.dao.currencies_dao import CurrenciesDAO
from src.dao.exchange_rates_dao import ExchangeRatesDAO
from src.database.sqlite_client import SQLiteClient
from src.services.service import Service


def main():
    f = open('src/database/config/config.json')
    ditc = json.load(f)
    db = SQLiteClient(ditc)

    exchange_rate_dao = ExchangeRatesDAO(db)
    currencies_dao = CurrenciesDAO(db)
    service = Service(currencies_dao, exchange_rate_dao)
    print(service.get_concrete_exchange_rate('RUBUSD'))


if __name__ == '__main__':
    main()
