from decimal import Decimal

from src.app.dao.currencies_dao import CurrenciesDAO
from src.app.dao.exchange_rates_dao import ExchangeRatesDAO
from src.app.database.sqlite_client import SQLiteClient
from src.app.dto.currency_dto import CurrencyDTO
from src.app.dto.exchange_rates_dto import ExchangeRatesDTO
from src.app.dto.exchanger_request import ExchangerRequest
from src.app.mappers.currency_mapper import CurrencyMapper
from src.app.mappers.exchange_rates_mapper import ExchangeRatesMapper
from src.app.services.currency_service import CurrencyService
from src.app.services.exchange_rates_service import ExchangeRatesService
import json

from src.app.services.exchanger_service import ExchangerService


def main():
    f = open('src/app/database/config/config.json')
    ditc = json.load(f)
    db = SQLiteClient(ditc)

    cur_dao = CurrenciesDAO(db)
    cur_mapper = CurrencyMapper()
    cur_service = CurrencyService(cur_dao, cur_mapper)

    ex_dao = ExchangeRatesDAO(db)
    ex_mapper = ExchangeRatesMapper()
    ex_service = ExchangeRatesService(ex_dao, ex_mapper)

    ex_rates_service = ExchangerService(ex_dao, cur_dao)

    exchanger_service = ExchangerService(ex_dao, cur_dao)

    print(exchanger_service.perform_currency_exchange(
        ExchangerRequest(cur_service.get_concrete_currency('CNY'), cur_service.get_concrete_currency('usd'),
                         Decimal(5))))


if __name__ == '__main__':
    main()
