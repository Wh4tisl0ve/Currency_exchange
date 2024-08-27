from dataclasses import dataclass


@dataclass(frozen=True)
class CurrencyDTO:
    ID: int
    name: str
    code: str
    sign: str
