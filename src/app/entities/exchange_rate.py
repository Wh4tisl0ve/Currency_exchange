from dataclasses import dataclass


@dataclass(frozen=True)
class ExchangeRate:
    id: int
    base_currency_id: int
    target_currency_id: int
    rate: float
