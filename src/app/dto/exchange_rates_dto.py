from dataclasses import dataclass
from decimal import Decimal

from src.app.dto.currency_dto import CurrencyDTO


@dataclass(frozen=True)
class ExchangeRatesDTO:
    id: int
    base_currency: CurrencyDTO
    target_currency: CurrencyDTO
    rate: Decimal
