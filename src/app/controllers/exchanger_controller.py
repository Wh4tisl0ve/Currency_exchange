from src.app.exceptions.exchanger.currency_identy_error import CurrencyIdentityError
from src.app.exceptions.db_error.database_error import DataBaseError
from src.app.exceptions.invalid_field_error import InvalidFieldError
from src.app.exceptions.not_found_error import NotFoundError
from src.app.services.exchanger_service import ExchangerService
from src.app.services.currency_service import CurrencyService
from src.app.dto.request.exchanger_request import ExchangerRequest
from src.app.router import Router
from decimal import Decimal, InvalidOperation


class ExchangerController:
    def __init__(self):
        self.__exchanger_service = ExchangerService()
        self.__currency_service = CurrencyService()
        self.register_routes()

    def register_routes(self):
        @Router().route(r'^/exchange$', method='GET')
        def get_all_exchange_rates(request: dict) -> dict:
            try:
                base_currency = self.__currency_service.get_concrete_currency(request['from'])
                target_currency = self.__currency_service.get_concrete_currency(request['to'])
                request = ExchangerRequest(base_currency=base_currency,
                                           target_currency=target_currency,
                                           amount=Decimal(str(request['amount']).replace(',', '.')))
                exchanger_response = self.__exchanger_service.perform_currency_exchange(request)
            except InvalidOperation:
                field_invalid = InvalidFieldError('The request contains invalid data')
                return field_invalid.to_dict()
            except KeyError:
                field_missing = InvalidFieldError('A required form field is missing')
                return field_missing.to_dict()
            except (NotFoundError, CurrencyIdentityError, DataBaseError) as err:
                return err.to_dict()

            return {"code": 200, "body": exchanger_response.to_dict()}
