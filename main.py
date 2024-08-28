import json

from src.dao.currencies_dao import CurrenciesDAO
from src.dao.exchange_rates_dao import ExchangeRatesDAO
from src.database.sqlite_client import SQLiteClient
from src.services.currency_service import CurrencyService
from src.services.exchange_rates_service import ExchangeRatesService


def main():
    f = open('src/database/config/config.json')
    ditc = json.load(f)
    db = SQLiteClient(ditc)

    exchange_rate_dao = ExchangeRatesDAO(db)
    currencies_dao = CurrenciesDAO(db)
    currency_service = CurrencyService(currencies_dao)
    exchange_rate_service = ExchangeRatesService(exchange_rate_dao, currencies_dao)
    print(exchange_rate_service.perform_currency_exchange('CNY','AUD', 1))


if __name__ == '__main__':
    main()
