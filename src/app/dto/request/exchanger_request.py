from src.app.dto.currency_dto import CurrencyDTO
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ExchangerRequest:
    base_currency: CurrencyDTO
    target_currency: CurrencyDTO
    amount: Decimal = Decimal(0)
