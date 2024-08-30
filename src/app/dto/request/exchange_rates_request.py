from dataclasses import dataclass


@dataclass(frozen=True)
class ExchangeRatesRequest:
    base_currency: str
    target_currency: str
    rate: float
