import json
from src.app.database.db_client import DBClient
from src.app.dto.currency_dto import CurrencyDTO
from src.app.dto.exchange_rates_dto import ExchangeRatesDTO
from src.app.router.router import Router
from src.app.services.currency_service import CurrencyService
from src.app.services.exchange_rates_service import ExchangeRatesService


class ExchangeRatesController:
    def __init__(self, db_client: DBClient, router: Router):
        self.__exchange_rates_service = ExchangeRatesService(db_client)
        self.__currency_service = CurrencyService(db_client)
        self.__router = router
        self.register_routes()

    def register_routes(self):
        @self.__router.route('/exchangeRates', method='GET')
        def get_all_exchange_rates() -> json:
            exchange_rates = self.__exchange_rates_service.get_all_exchange_rates()
            return json.dumps([ex_r.to_dict() for ex_r in exchange_rates], indent=4)

        @self.__router.route(r'^/exchangeRate/(?P<currency_pair>[a-zA-Z]{6})$', method='GET')
        def get_concrete_exchange_rate(currency_pair: str):
            base_currency = self.__currency_service.get_concrete_currency(currency_pair[:3])
            target_currency = self.__currency_service.get_concrete_currency(currency_pair[3:])

            request = ExchangeRatesDTO(base_currency=base_currency, target_currency=target_currency)
            exchange_rate = self.__exchange_rates_service.get_exchange_rate(request)

            result_exchange_rate = ExchangeRatesDTO(id=exchange_rate.id,
                                                    base_currency=base_currency,
                                                    target_currency=target_currency,
                                                    rate=exchange_rate.rate)
            return json.dumps(result_exchange_rate.to_dict(), indent=4)

        @self.__router.route('/currencies', method='POST')
        def add_currency(request: dict):
            currency_request = CurrencyDTO(id=0,
                                           name=request.get('name'),
                                           code=request.get('code'),
                                           sign=request.get('sign'))
            added_currency = self.__exchange_rates_service.add_currency(currency_request)
            return json.dumps(added_currency.to_dict(), indent=4)
