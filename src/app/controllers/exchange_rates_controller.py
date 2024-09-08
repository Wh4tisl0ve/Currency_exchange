from src.app.exceptions.exchange_rates_error.exchange_rate_already_exists_error import ExchangeRateAlreadyExistsError
from src.app.exceptions.exchange_rates_error.exchange_rates_not_found_error import ExchangeRateNotFoundError
from src.app.exceptions.currency_error.currency_not_found_error import CurrencyNotFoundError
from src.app.exceptions.exchange_rates_error.invalid_currency_pair_error import InvalidCurrencyPairError
from src.app.exceptions.invalid_field_error import InvalidFieldError
from src.app.exceptions.required_field_missing_error import RequiredFieldMissingError
from src.app.exceptions.no_content_error import NoContentError
from src.app.services.currency_service import CurrencyService
from src.app.services.exchange_rates_service import ExchangeRatesService
from src.app.dto.exchange_rates_dto import ExchangeRatesDTO
from src.app.router import Router
from decimal import Decimal, InvalidOperation


class ExchangeRatesController:
    def __init__(self):
        self.__exchange_rates_service = ExchangeRatesService()
        self.__currency_service = CurrencyService()
        self.__router = Router()
        self.register_routes()

    def register_routes(self):
        @self.__router.route(r'^/exchangeRates$', method='GET')
        def get_all_exchange_rates() -> dict:
            try:
                exchange_rates = self.__exchange_rates_service.get_all_exchange_rates()
            except NoContentError as no_content:
                return no_content.to_dict()

            return {"code": 200, "body": [ex_r.to_dict() for ex_r in exchange_rates]}

        @self.__router.route(r'^/exchangeRate/(?P<currency_pair>[a-zA-Z]{6})$', method='GET')
        def get_concrete_exchange_rate(currency_pair: str) -> dict:
            try:
                base_currency = self.__currency_service.get_concrete_currency(currency_pair[:3])
                target_currency = self.__currency_service.get_concrete_currency(currency_pair[3:])

                request = ExchangeRatesDTO(base_currency=base_currency, target_currency=target_currency)
                exchange_rate = self.__exchange_rates_service.get_exchange_rate(request)
            except (CurrencyNotFoundError, ExchangeRateNotFoundError) as e:
                return e.to_dict()

            result_exchange_rate = ExchangeRatesDTO(id=exchange_rate.id,
                                                    base_currency=base_currency,
                                                    target_currency=target_currency,
                                                    rate=exchange_rate.rate)

            return {"code": 200, "body": result_exchange_rate.to_dict()}

        @self.__router.route(r'^/exchangeRates$', method='POST')
        def add_exchange_rates(request: dict) -> dict:
            try:
                base_currency = self.__currency_service.get_concrete_currency(request['baseCurrencyCode'])
                target_currency = self.__currency_service.get_concrete_currency(request['targetCurrencyCode'])

                request_dto = ExchangeRatesDTO(base_currency=base_currency,
                                               target_currency=target_currency,
                                               rate=Decimal(str(request['rate']).replace(',', '.')))

                added_exchange_rate = self.__exchange_rates_service.add_exchange_rate(request_dto)
            except InvalidOperation:
                field_invalid = InvalidFieldError('Запрос содержит некорректные данные')
                return field_invalid.to_dict()
            except KeyError:
                field_missing = RequiredFieldMissingError('Отсутствует нужное поле формы', 400)
                return field_missing.to_dict()
            except (CurrencyNotFoundError, ExchangeRateAlreadyExistsError, InvalidCurrencyPairError) as e:
                return e.to_dict()

            result_exchange_rate = ExchangeRatesDTO(id=added_exchange_rate.id,
                                                    base_currency=base_currency,
                                                    target_currency=target_currency,
                                                    rate=added_exchange_rate.rate)

            return {"code": 201, "body": result_exchange_rate.to_dict()}

        @self.__router.route(r'^/exchangeRate/(?P<currency_pair>[a-zA-Z]{6})$', method='PATCH')
        def update_exchange_rate(request: dict) -> dict:
            currency_pair = request['path'].split('/')[-1]
            try:
                base_currency = self.__currency_service.get_concrete_currency(currency_pair[:3])
                target_currency = self.__currency_service.get_concrete_currency(currency_pair[3:])

                request_dto = ExchangeRatesDTO(base_currency=base_currency,
                                               target_currency=target_currency,
                                               rate=Decimal(str(request['rate']).replace(',', '.')))
                updated_exchange_rate = self.__exchange_rates_service.update_exchange_rate(request_dto)
            except (CurrencyNotFoundError, ExchangeRateNotFoundError) as e:
                return e.to_dict()
            except InvalidOperation:
                field_invalid = InvalidFieldError('Запрос содержит некорректные данные')
                return field_invalid.to_dict()
            except KeyError:
                field_missing = RequiredFieldMissingError('Отсутствует нужное поле формы', 400)
                return field_missing.to_dict()

            result_exchange_rate = ExchangeRatesDTO(id=updated_exchange_rate.id,
                                                    base_currency=base_currency,
                                                    target_currency=target_currency,
                                                    rate=updated_exchange_rate.rate)

            return {"code": 200, "body": result_exchange_rate.to_dict()}
