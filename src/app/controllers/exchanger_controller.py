import json
from decimal import Decimal

from src.app.database.db_client import DBClient
from src.app.dto.request.exchanger_request import ExchangerRequest
from src.app.exceptions.currency_error.currency_not_found_error import CurrencyNotFoundError
from src.app.exceptions.exchange_rates_error.exchange_rates_not_found_error import ExchangeRateNotFoundError
from src.app.exceptions.required_field_missing_error import RequiredFieldMissingError
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
            try:
                base_currency = self.__currency_service.get_concrete_currency(request['from'])
                target_currency = self.__currency_service.get_concrete_currency(request['to'])
                request = ExchangerRequest(base_currency=base_currency,
                                           target_currency=target_currency,
                                           amount=Decimal(request['amount']))
                exchanger_response = self.__exchanger_service.perform_currency_exchange(request)
            except KeyError:
                field_missing = RequiredFieldMissingError('Отсутствует нужный параметр', 400)
                return json.dumps(field_missing.to_dict(), indent=4)
            except CurrencyNotFoundError as currency_not_found:
                return json.dumps(currency_not_found.to_dict(), indent=4)
            except ExchangeRateNotFoundError as exchange_rate_not_found:
                return json.dumps(exchange_rate_not_found.to_dict(), indent=4)

            return json.dumps(exchanger_response.to_dict(), indent=4)
