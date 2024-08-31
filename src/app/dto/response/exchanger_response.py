from src.app.dto.currency_dto import CurrencyDTO
from dataclasses import dataclass


@dataclass(frozen=True)
class ExchangerResponse:
    base_currency: CurrencyDTO
    target_currency: CurrencyDTO
    rate: float
    amount: float
    converted_amount: float

