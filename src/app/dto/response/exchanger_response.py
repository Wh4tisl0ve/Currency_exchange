from dataclasses import dataclass

from src.app.dto.response.currency_response import CurrencyResponse


@dataclass(frozen=True)
class ExchangerResponse:
    base_currency: CurrencyResponse
    target_currency: CurrencyResponse
    rate: float
    amount: float
    converted_amount: float

