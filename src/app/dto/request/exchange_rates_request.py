from dataclasses import dataclass

from src.app.dto.response.currency_response import CurrencyResponse


@dataclass(frozen=True)
class ExchangeRatesRequest:
    base_currency: str
    target_currency: str
    rate: float
