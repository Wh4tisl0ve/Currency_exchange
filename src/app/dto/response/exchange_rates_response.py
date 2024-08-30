from dataclasses import dataclass

from src.app.dto.currency_dto import CurrencyDTO


@dataclass(frozen=True)
class ExchangeRatesResponse:
    id: int
    base_currency: CurrencyDTO
    target_currency: CurrencyDTO
    rate: float
