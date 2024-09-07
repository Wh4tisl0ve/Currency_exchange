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

    def to_dict(self):
        return {"baseCurrency": self.base_currency.to_dict(),
                "targetCurrency": self.target_currency.to_dict(),
                "rate": float(self.rate),
                "amount": float(self.amount),
                "convertedAmount": float(self.converted_amount)}
