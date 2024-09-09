from src.app.exceptions.exchange_rates_error.exchange_rates_not_found_error import ExchangeRateNotFoundError
from src.app.exceptions.currency_error.currency_not_found_error import CurrencyNotFoundError
from src.app.exceptions.required_field_missing_error import RequiredFieldMissingError
from src.app.exceptions.exchanger.currency_identy_error import CurrencyIdentityError
from src.app.exceptions.invalid_field_error import InvalidFieldError
from src.app.exceptions.not_found_error import NotFoundError
from src.app.services.currency_service import CurrencyService
from src.app.services.exchanger_service import ExchangerService
from src.app.dto.request.exchanger_request import ExchangerRequest
from src.app.router import Router
from decimal import Decimal, InvalidOperation


class ExchangerController:
    def __init__(self, exchanger_service: ExchangerService, currency_service: CurrencyService):
        self.__exchanger_service = exchanger_service
        self.__currency_service = currency_service
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
                field_invalid = InvalidFieldError('Запрос содержит некорректные данные')
                return field_invalid.to_dict()
            except KeyError:
                field_missing = RequiredFieldMissingError('Отсутствует нужный параметр', 400)
                return field_missing.to_dict()
            except (CurrencyNotFoundError,
                    ExchangeRateNotFoundError,
                    NotFoundError,
                    CurrencyIdentityError) as e:
                return e.to_dict()

            return {"code": 200, "body": exchanger_response.to_dict()}
