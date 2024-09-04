from dataclasses import dataclass


@dataclass(frozen=True)
class CurrencyDTO:
    id: int = 0
    name: str = ''
    code: str = ''
    sign: str = ''

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "sign": self.sign
        }
