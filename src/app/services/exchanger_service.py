from decimal import Decimal

from src.app.dao.currencies_dao import CurrenciesDAO
from src.app.dao.exchange_rates_dao import ExchangeRatesDAO
from src.app.dto.request.exchanger_request import ExchangerRequest
from src.app.dto.response.exchanger_response import ExchangerResponse
from src.app.entities.exchange_rate import ExchangeRate


class ExchangerService:
    def __init__(self, exchange_rates_dao: ExchangeRatesDAO, currencies_dao: CurrenciesDAO):
        self.__exchange_rates_dao = exchange_rates_dao
        self.__currencies_dao = currencies_dao

    def perform_currency_exchange(self, exchanger_request: ExchangerRequest) -> ExchangerResponse:
        base_currency_id = exchanger_request.base_currency.id
        target_currency_id = exchanger_request.target_currency.id
        amount = Decimal(exchanger_request.amount)

        direct_exchange_rate_entity = self.__get_exchange_rate(base_currency_id, target_currency_id)
        reverse_exchange_rate_entity = self.__get_exchange_rate(target_currency_id, base_currency_id)

        direct_exchange_rate = self.__exchange_rates_dao.get_exchange_rate(direct_exchange_rate_entity)
        reverse_exchange_rate = self.__exchange_rates_dao.get_exchange_rate(reverse_exchange_rate_entity)

        if direct_exchange_rate:
            converted_amount = Decimal(direct_exchange_rate.rate) * amount
            rate = direct_exchange_rate.rate
        elif reverse_exchange_rate:
            converted_amount = amount / reverse_exchange_rate.rate
            rate = reverse_exchange_rate.rate
        else:
            converted_amount = self.__calc_amount_via_usd(exchanger_request)
            rate = converted_amount / amount

        converted_amount = converted_amount.quantize(Decimal('0.00001'))
        return ExchangerResponse(exchanger_request.base_currency,
                                 exchanger_request.target_currency,
                                 rate,
                                 exchanger_request.amount,
                                 converted_amount)

    def __calc_amount_via_usd(self, exchanger_request: ExchangerRequest) -> Decimal:
        usd_currency = self.__currencies_dao.get_currency_by_code('USD')

        direct_exchange_rate_entity = self.__get_exchange_rate(exchanger_request.base_currency.id, usd_currency.id)
        reverse_exchange_rate_entity = self.__get_exchange_rate(exchanger_request.target_currency.id, usd_currency.id)

        base_usd_exchange_rate = self.__exchange_rates_dao.get_exchange_rate(direct_exchange_rate_entity)
        target_usd_exchange_rate = self.__exchange_rates_dao.get_exchange_rate(reverse_exchange_rate_entity)

        converted_amount = (exchanger_request.amount * base_usd_exchange_rate.rate) * target_usd_exchange_rate.rate
        return converted_amount

    def __get_exchange_rate(self, base_currency_id: int, target_currency_id: int) -> ExchangeRate:
        exchange_rate_entity = ExchangeRate(id=0,
                                            base_currency_id=base_currency_id,
                                            target_currency_id=target_currency_id,
                                            rate=Decimal(0))
        return self.__exchange_rates_dao.get_exchange_rate(exchange_rate_entity)

