from dataclasses import dataclass


@dataclass(frozen=True)
class CurrencyResponse:
    id: int
    name: str
    code: str
    sign: str
