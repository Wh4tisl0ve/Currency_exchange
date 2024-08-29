import json
from src.app.dao.currencies_dao import CurrenciesDAO
from src.app.dao.exchange_rates_dao import ExchangeRatesDAO
from src.app.database.sqlite_client import SQLiteClient
from src.app.mappers.exchange_rates_mapper import ExchangeRatesMapper
from src.app.services.exchange_rates_service import ExchangeRatesService


def main():
    f = open('src/app/database/config/config.json')
    ditc = json.load(f)
    db = SQLiteClient(ditc)

    currencies_dao = CurrenciesDAO(db)
    ex_dao = ExchangeRatesDAO(db)
    cur_mapper = ExchangeRatesMapper()
    ex_service = ExchangeRatesService(ex_dao, currencies_dao, cur_mapper)
    ex_service.get_all_exchange_rates()


if __name__ == '__main__':
    main()
