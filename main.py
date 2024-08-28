import json

from src.DAO.currencies_dao import CurrenciesDAO
from src.DAO.exchange_rates_dao import ExchangeRatesDAO
from src.Database.sqlite_client import SQLiteClient
from src.Services.sevice import Service


def main():
    f = open('src/database/config/config.json')
    ditc = json.load(f)
    db = SQLiteClient(ditc)

    exchange_rate_dao = ExchangeRatesDAO(db)
    currencies_dao = CurrenciesDAO(db)
    service = Service(currencies_dao, exchange_rate_dao)
    service.get_concrete_exchange_rate('AUDRUB')


if __name__ == '__main__':
    main()
