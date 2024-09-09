from src.app.exceptions.exchanger.currency_identy_error import CurrencyIdentityError
from src.app.exceptions.not_found_error import NotFoundError
from src.app.dto.response.exchanger_response import ExchangerResponse
from src.app.dto.request.exchanger_request import ExchangerRequest
from src.app.dao.exchange_rate_dao import ExchangeRateDAO
from src.app.dao.currency_dao import CurrencyDAO
from src.app.entities.exchange_rate import ExchangeRate
from decimal import Decimal


class ExchangerService:
    def __init__(self):
        self.__exchange_rates_dao = ExchangeRateDAO()
        self.__currencies_dao = CurrencyDAO()

    def perform_currency_exchange(self, exchanger_request: ExchangerRequest) -> ExchangerResponse:
        if exchanger_request.base_currency.id == exchanger_request.target_currency.id:
            raise CurrencyIdentityError('Невозможно обменять валюту на саму себя')

        try:
            return self.__calc_by_direct_rate(exchanger_request)
        except NotFoundError:
            try:
                return self.__calc_by_reverse_rate(exchanger_request)
            except NotFoundError:
                return self.__calc_by_cross_rate(exchanger_request)

    def __calc_by_direct_rate(self, exchanger_request: ExchangerRequest):
        direct_exchange_rate_entity = self.__get_entity(exchanger_request.base_currency.id,
                                                        exchanger_request.target_currency.id)
        direct_exchange_rate = self.__exchange_rates_dao.find_by_pair_id(direct_exchange_rate_entity)

        converted_amount = direct_exchange_rate.rate * exchanger_request.amount
        rate = direct_exchange_rate.rate

        return ExchangerResponse(exchanger_request.base_currency,
                                 exchanger_request.target_currency,
                                 rate.quantize(Decimal('0.001')),
                                 exchanger_request.amount,
                                 converted_amount.quantize(Decimal('0.01')))

    def __calc_by_reverse_rate(self, exchanger_request: ExchangerRequest):
        reverse_exchange_rate_entity = self.__get_entity(exchanger_request.target_currency.id,
                                                         exchanger_request.base_currency.id)
        reverse_exchange_rate = self.__exchange_rates_dao.find_by_pair_id(reverse_exchange_rate_entity)
        rate = Decimal(1) / reverse_exchange_rate.rate
        converted_amount = exchanger_request.amount * rate

        return ExchangerResponse(exchanger_request.base_currency,
                                 exchanger_request.target_currency,
                                 rate.quantize(Decimal('0.0001')),
                                 exchanger_request.amount,
                                 converted_amount.quantize(Decimal('0.01')))

    def __calc_by_cross_rate(self, exchanger_request: ExchangerRequest):
        usd_currency = self.__currencies_dao.find_by_code('USD')

        usd_base_exchange_rate_entity = self.__get_entity(usd_currency.id, exchanger_request.base_currency.id)
        usd_target_exchange_rate_entity = self.__get_entity(usd_currency.id, exchanger_request.target_currency.id)

        usd_base_exchange_rate = self.__exchange_rates_dao.find_by_pair_id(usd_base_exchange_rate_entity)
        usd_target_exchange_rate = self.__exchange_rates_dao.find_by_pair_id(usd_target_exchange_rate_entity)

        converted_amount = (usd_base_exchange_rate.rate / usd_target_exchange_rate.rate) * exchanger_request.amount
        rate = converted_amount / exchanger_request.amount

        return ExchangerResponse(exchanger_request.base_currency,
                                 exchanger_request.target_currency,
                                 rate.quantize(Decimal('0.0001')),
                                 exchanger_request.amount,
                                 converted_amount.quantize(Decimal('0.01')))

    def __get_entity(self, base_currency_id: int, target_currency_id: int) -> ExchangeRate:
        exchange_rate_entity = ExchangeRate(id=0,
                                            base_currency_id=base_currency_id,
                                            target_currency_id=target_currency_id,
                                            rate=Decimal(0))
        return self.__exchange_rates_dao.find_by_pair_id(exchange_rate_entity)
