from dataclasses import dataclass


@dataclass(frozen=True)
class CurrencyRequest:
    name: str
    code: str
    sign: str
