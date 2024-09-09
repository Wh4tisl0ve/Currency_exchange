from src.app.exceptions.constraint_violation_error import ConstraintViolationException
from src.app.exceptions.invalid_field_error import InvalidFieldError
from src.app.exceptions.not_found_error import NotFoundError
from src.app.exceptions.no_content_error import NoContentError
from src.app.services.currency_service import CurrencyService
from src.app.services.exchange_rate_service import ExchangeRateService
from src.app.dto.exchange_rate_dto import ExchangeRateDTO
from src.app.router import Router
from decimal import Decimal, InvalidOperation


class ExchangeRateController:
    def __init__(self):
        self.__exchange_rates_service = ExchangeRateService()
        self.__currency_service = CurrencyService()
        self.register_routes()

    def register_routes(self):
        @Router().route(r'^/exchangeRates$', method='GET')
        def get_all_exchange_rates() -> dict:
            try:
                exchange_rates = self.__exchange_rates_service.get_all_exchange_rates()
            except NoContentError as no_content:
                return no_content.to_dict()

            return {"code": 200, "body": [ex_r.to_dict() for ex_r in exchange_rates]}

        @Router().route(r'^/exchangeRate/(?P<currency_pair>[a-zA-Z]{6})$', method='GET')
        def get_concrete_exchange_rate(currency_pair: str) -> dict:
            try:
                base_currency = self.__currency_service.get_concrete_currency(currency_pair[:3])
                target_currency = self.__currency_service.get_concrete_currency(currency_pair[3:])

                request = ExchangeRateDTO(base_currency=base_currency, target_currency=target_currency)
                exchange_rate = self.__exchange_rates_service.get_exchange_rate(request)
            except NotFoundError as not_found_error:
                return not_found_error.to_dict()

            result_exchange_rate = ExchangeRateDTO(id=exchange_rate.id,
                                                   base_currency=base_currency,
                                                   target_currency=target_currency,
                                                   rate=exchange_rate.rate)

            return {"code": 200, "body": result_exchange_rate.to_dict()}

        @Router().route(r'^/exchangeRates$', method='POST')
        def add_exchange_rates(request: dict) -> dict:
            try:
                base_currency = self.__currency_service.get_concrete_currency(request['baseCurrencyCode'])
                target_currency = self.__currency_service.get_concrete_currency(request['targetCurrencyCode'])

                request_dto = ExchangeRateDTO(base_currency=base_currency,
                                              target_currency=target_currency,
                                              rate=Decimal(str(request['rate']).replace(',', '.')))

                added_exchange_rate = self.__exchange_rates_service.add_exchange_rate(request_dto)
            except InvalidOperation:
                field_invalid = InvalidFieldError('The request contains invalid data')
                return field_invalid.to_dict()
            except KeyError:
                field_missing = InvalidFieldError('A required form field is missing')
                return field_missing.to_dict()
            except (NotFoundError, ConstraintViolationException) as e:
                return e.to_dict()

            result_exchange_rate = ExchangeRateDTO(id=added_exchange_rate.id,
                                                   base_currency=base_currency,
                                                   target_currency=target_currency,
                                                   rate=added_exchange_rate.rate)

            return {"code": 201, "body": result_exchange_rate.to_dict()}

        @Router().route(r'^/exchangeRate/(?P<currency_pair>[a-zA-Z]{6})$', method='PATCH')
        def update_exchange_rate(request: dict) -> dict:
            currency_pair = request['path'].split('/')[-1]
            try:
                base_currency = self.__currency_service.get_concrete_currency(currency_pair[:3])
                target_currency = self.__currency_service.get_concrete_currency(currency_pair[3:])

                request_dto = ExchangeRateDTO(base_currency=base_currency,
                                              target_currency=target_currency,
                                              rate=Decimal(str(request['rate']).replace(',', '.')))
                updated_exchange_rate = self.__exchange_rates_service.update_exchange_rate(request_dto)
            except NotFoundError as not_found_error:
                return not_found_error.to_dict()
            except InvalidOperation:
                field_invalid = InvalidFieldError('The request contains invalid data')
                return field_invalid.to_dict()
            except KeyError:
                field_missing = InvalidFieldError('A required form field is missing')
                return field_missing.to_dict()

            result_exchange_rate = ExchangeRateDTO(id=updated_exchange_rate.id,
                                                   base_currency=base_currency,
                                                   target_currency=target_currency,
                                                   rate=updated_exchange_rate.rate)

            return {"code": 200, "body": result_exchange_rate.to_dict()}
