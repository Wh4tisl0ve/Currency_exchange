from dataclasses import dataclass


@dataclass
class ExchangeRatesDTO:
    id: int
    base_currency_id: int
    target_currency_id: int
    rate: float
