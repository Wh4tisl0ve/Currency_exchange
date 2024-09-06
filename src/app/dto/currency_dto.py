from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class CurrencyDTO:
    id: int = 0
    name: str = ''
    code: str = ''
    sign: str = ''

    def to_dict(self) -> dict:
        return asdict(self)
