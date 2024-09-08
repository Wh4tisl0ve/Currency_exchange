from src.app.dto.currency_dto import CurrencyDTO
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ExchangeRatesDTO:
    base_currency: CurrencyDTO
    target_currency: CurrencyDTO
    id: int = 0
    rate: Decimal = Decimal(0)

    def to_dict(self) -> dict:
        return {"id": self.id,
                "baseCurrency": self.base_currency.to_dict(),
                "targetCurrency": self.target_currency.to_dict(),
                "rate": float(self.rate)
                }
