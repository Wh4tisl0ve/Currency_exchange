from decimal import Decimal

from src.app.dto.currency_dto import CurrencyDTO
from dataclasses import dataclass


@dataclass(frozen=True)
class ExchangerResponse:
    base_currency: CurrencyDTO
    target_currency: CurrencyDTO
    rate: Decimal
    amount: Decimal
    converted_amount: Decimal

