import json
from decimal import Decimal

from src.app.database.db_client import DBClient
from src.app.dto.exchange_rates_dto import ExchangeRatesDTO
from src.app.dto.request.exchanger_request import ExchangerRequest
from src.app.router.router import Router
from src.app.services.currency_service import CurrencyService
from src.app.services.exchanger_service import ExchangerService


class ExchangerController:
    def __init__(self, db_client: DBClient, router: Router):
        self.__exchanger_service = ExchangerService(db_client)
        self.__currency_service = CurrencyService(db_client)
        self.__router = router
        self.register_routes()

    def register_routes(self):
        @self.__router.route('/exchange', method='GET')
        def get_all_exchange_rates(request: dict) -> json:
            base_currency = self.__currency_service.get_concrete_currency(request.get('from'))
            target_currency = self.__currency_service.get_concrete_currency(request.get('to'))
            request = ExchangerRequest(base_currency=base_currency,
                                       target_currency=target_currency,
                                       amount=Decimal(request.get('amount')))
            exchanger_response = self.__exchanger_service.perform_currency_exchange(request)
            return json.dumps(exchanger_response.to_dict(), indent=4)


