import json

from app.dao.currencies_dao import CurrenciesDAO
from app.dao.exchange_rates_dao import ExchangeRatesDAO
from app.database.sqlite_client import SQLiteClient
from app.services.currency_service import CurrencyService
from app.services.exchange_rates_service import ExchangeRatesService


def main():
    f = open('app/database/config/config.json')
    ditc = json.load(f)
    db = SQLiteClient(ditc)

    exchange_rate_dao = ExchangeRatesDAO(db)
    currencies_dao = CurrenciesDAO(db)
    currency_service = CurrencyService(currencies_dao)
    exchange_rate_service = ExchangeRatesService(exchange_rate_dao, currencies_dao)
    print(exchange_rate_service.perform_currency_exchange('CNY', 'AUD', 1))


if __name__ == '__main__':
    main()
