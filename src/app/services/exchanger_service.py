def perform_currency_exchange(self, base_currency: CurrencyResponse, target_currency: CurrencyResponse,
                              amount: float) -> ExchangerResponse:
    direct_exchange_rate = self.get_exchange_rate(base_currency, target_currency)
    reverse_exchange_rate = self.get_exchange_rate(target_currency, base_currency)

    if direct_exchange_rate is not None:
        converted_amount = direct_exchange_rate.rate * amount
        rate = direct_exchange_rate.rate
    elif reverse_exchange_rate is not None:
        converted_amount = amount / reverse_exchange_rate.rate
        rate = reverse_exchange_rate.rate
    else:
        converted_amount = self.exchange_via_usd(base_currency, target_currency, amount)
        rate = converted_amount / amount

    return ExchangerResponse(base_currency, target_currency, rate, amount, converted_amount)


def exchange_via_usd(self, base_currency: CurrencyResponse, target_currency: CurrencyResponse,
                     amount: float) -> float:
    usd_currency = self.__currencies_dao.get_currency_by_code('USD')
    base_usd_exchange_rate = self.__exchange_rates_dao.get_exchange_rate(base_currency.id, usd_currency.id)
    target_usd_exchange_rate = self.__exchange_rates_dao.get_exchange_rate(usd_currency.id, target_currency.id)

    converted_amount = (amount * base_usd_exchange_rate.rate) * target_usd_exchange_rate.rate
    return converted_amount