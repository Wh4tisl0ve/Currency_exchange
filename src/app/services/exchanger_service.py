from src.app.exceptions.exchange_rates_error.exchange_rates_not_found_error import ExchangeRateNotFoundError
from src.app.exceptions.exchanger.currency_identy_error import CurrencyIdentityError
from src.app.exceptions.not_found_error import NotFoundError
from src.app.dto.response.exchanger_response import ExchangerResponse
from src.app.dto.request.exchanger_request import ExchangerRequest
from src.app.dao.exchange_rates_dao import ExchangeRatesDAO
from src.app.dao.currencies_dao import CurrenciesDAO
from src.app.database.db_client import DBClient
from src.app.entities.exchange_rate import ExchangeRate
from decimal import Decimal


class ExchangerService:
    def __init__(self, db_client: DBClient):
        self.__exchange_rates_dao = ExchangeRatesDAO(db_client)
        self.__currencies_dao = CurrenciesDAO(db_client)

    def perform_currency_exchange(self, exchanger_request: ExchangerRequest) -> ExchangerResponse:
        if exchanger_request.base_currency.id == exchanger_request.target_currency.id:
            raise CurrencyIdentityError('Невозможно обменять валюту на саму себя')

        return self.__calc_via_direct_exchange_rate(exchanger_request)

    def __calc_via_direct_exchange_rate(self, exchanger_request: ExchangerRequest):
        try:
            direct_exchange_rate_entity = self.__get_entity(exchanger_request.base_currency.id,
                                                            exchanger_request.target_currency.id)
            direct_exchange_rate = self.__exchange_rates_dao.get_exchange_rate(direct_exchange_rate_entity)

            converted_amount = direct_exchange_rate.rate * exchanger_request.amount
            rate = direct_exchange_rate.rate

            return ExchangerResponse(exchanger_request.base_currency,
                                     exchanger_request.target_currency,
                                     rate.quantize(Decimal('0.0001')),
                                     exchanger_request.amount,
                                     converted_amount.quantize(Decimal('0.0001')))
        except ExchangeRateNotFoundError:
            return self.__calc_via_reverse_exchange_rate(exchanger_request)

    def __calc_via_reverse_exchange_rate(self, exchanger_request: ExchangerRequest):
        try:
            reverse_exchange_rate_entity = self.__get_entity(exchanger_request.target_currency.id,
                                                             exchanger_request.base_currency.id)
            reverse_exchange_rate = self.__exchange_rates_dao.get_exchange_rate(reverse_exchange_rate_entity)

            rate = 1 / reverse_exchange_rate.rate
            converted_amount = exchanger_request.amount * rate

            return ExchangerResponse(exchanger_request.base_currency,
                                     exchanger_request.target_currency,
                                     rate.quantize(Decimal('0.0001')),
                                     exchanger_request.amount,
                                     converted_amount.quantize(Decimal('0.0001')))
        except ExchangeRateNotFoundError:
            return self.__calc_amount_via_usd(exchanger_request)

    def __calc_amount_via_usd(self, exchanger_request: ExchangerRequest):
        try:
            usd_currency = self.__currencies_dao.get_currency_by_code('USD')

            usd_base_exchange_rate_entity = self.__get_entity(usd_currency.id, exchanger_request.base_currency.id)
            usd_target_exchange_rate_entity = self.__get_entity(usd_currency.id, exchanger_request.target_currency.id)

            usd_base_exchange_rate = self.__exchange_rates_dao.get_exchange_rate(usd_base_exchange_rate_entity)
            usd_target_exchange_rate = self.__exchange_rates_dao.get_exchange_rate(usd_target_exchange_rate_entity)

            converted_amount = (usd_base_exchange_rate.rate / usd_target_exchange_rate.rate) * exchanger_request.amount
            rate = converted_amount / exchanger_request.amount

            return ExchangerResponse(exchanger_request.base_currency,
                                     exchanger_request.target_currency,
                                     rate.quantize(Decimal('0.0001')),
                                     exchanger_request.amount,
                                     converted_amount.quantize(Decimal('0.0001')))
        except ExchangeRateNotFoundError:
            raise NotFoundError('Не найден обменный курс для валютной пары')

    def __get_entity(self, base_currency_id: int, target_currency_id: int) -> ExchangeRate:
        exchange_rate_entity = ExchangeRate(id=0,
                                            base_currency_id=base_currency_id,
                                            target_currency_id=target_currency_id,
                                            rate=Decimal(0))
        return self.__exchange_rates_dao.get_exchange_rate(exchange_rate_entity)
