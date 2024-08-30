from dataclasses import dataclass


@dataclass(frozen=True)
class CurrencyDTO:
    id: int
    name: str
    code: str
    sign: str
