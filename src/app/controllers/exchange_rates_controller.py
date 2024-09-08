from src.app.exceptions.exchange_rates_error.exchange_rates_not_found_error import ExchangeRateNotFoundError
from src.app.exceptions.exchange_rates_error.exchange_rate_already_exists_error import ExchangeRateAlreadyExistsError
from src.app.exceptions.currency_error.currency_not_found_error import CurrencyNotFoundError
from src.app.exceptions.required_field_missing_error import RequiredFieldMissingError
from src.app.exceptions.no_content_error import NoContentError
from src.app.services.currency_service import CurrencyService
from src.app.services.exchange_rates_service import ExchangeRatesService
from src.app.dto.exchange_rates_dto import ExchangeRatesDTO
from src.app.database.db_client import DBClient
from src.app.router.router import Router
import json


class ExchangeRatesController:
    def __init__(self, db_client: DBClient, router: Router):
        self.__exchange_rates_service = ExchangeRatesService(db_client)
        self.__currency_service = CurrencyService(db_client)
        self.__router = router
        self.register_routes()

    def register_routes(self):
        @self.__router.route(r'^/exchangeRates$', method='GET')
        def get_all_exchange_rates() -> json:
            try:
                exchange_rates = self.__exchange_rates_service.get_all_exchange_rates()
            except NoContentError as no_content:
                return json.dumps(no_content.to_dict(), indent=4)

            return json.dumps([ex_r.to_dict() for ex_r in exchange_rates], indent=4)

        @self.__router.route(r'^/exchangeRate/(?P<currency_pair>[a-zA-Z]{6})$', method='GET')
        def get_concrete_exchange_rate(currency_pair: str):
            try:
                base_currency = self.__currency_service.get_concrete_currency(currency_pair[:3])
                target_currency = self.__currency_service.get_concrete_currency(currency_pair[3:])

                request = ExchangeRatesDTO(base_currency=base_currency, target_currency=target_currency)
                exchange_rate = self.__exchange_rates_service.get_exchange_rate(request)
            except (CurrencyNotFoundError, ExchangeRateNotFoundError) as e:
                return json.dumps(e.to_dict(), indent=4)

            result_exchange_rate = ExchangeRatesDTO(id=exchange_rate.id,
                                                    base_currency=base_currency,
                                                    target_currency=target_currency,
                                                    rate=exchange_rate.rate)

            return json.dumps(result_exchange_rate.to_dict(), indent=4)

        @self.__router.route(r'^/exchangeRates$', method='POST')
        def add_exchange_rates(request: dict):
            try:
                base_currency = self.__currency_service.get_concrete_currency(request['baseCurrencyCode'])
                target_currency = self.__currency_service.get_concrete_currency(request['targetCurrencyCode'])

                request_dto = ExchangeRatesDTO(base_currency=base_currency,
                                               target_currency=target_currency,
                                               rate=request['rate'])

                added_exchange_rate = self.__exchange_rates_service.add_exchange_rate(request_dto)
            except KeyError:
                field_missing = RequiredFieldMissingError('Отсутствует нужное поле формы', 400)
                return json.dumps(field_missing.to_dict(), indent=4)
            except (CurrencyNotFoundError, ExchangeRateAlreadyExistsError) as e:
                return json.dumps(e.to_dict(), indent=4)

            result_exchange_rate = ExchangeRatesDTO(id=added_exchange_rate.id,
                                                    base_currency=base_currency,
                                                    target_currency=target_currency,
                                                    rate=added_exchange_rate.rate)

            return json.dumps(result_exchange_rate.to_dict(), indent=4)

        @self.__router.route(r'^/exchangeRate/(?P<currency_pair>[a-zA-Z]{6})$', method='PATCH')
        def update_exchange_rate(request: dict):
            currency_pair = request['path'].split('/')[-1]
            try:
                base_currency = self.__currency_service.get_concrete_currency(currency_pair[:3])
                target_currency = self.__currency_service.get_concrete_currency(currency_pair[3:])

                request_dto = ExchangeRatesDTO(base_currency=base_currency,
                                               target_currency=target_currency,
                                               rate=request['rate'])
                updated_exchange_rate = self.__exchange_rates_service.update_exchange_rate(request_dto)
            except KeyError:
                field_missing = RequiredFieldMissingError('Отсутствует нужное поле формы', 400)
                return json.dumps(field_missing.to_dict(), indent=4)
            except (CurrencyNotFoundError, ExchangeRateNotFoundError) as e:
                return json.dumps(e.to_dict(), indent=4)

            result_exchange_rate = ExchangeRatesDTO(id=updated_exchange_rate.id,
                                                    base_currency=base_currency,
                                                    target_currency=target_currency,
                                                    rate=updated_exchange_rate.rate)

            return json.dumps(result_exchange_rate.to_dict(), indent=4)
