from dataclasses import dataclass


@dataclass(frozen=True)
class Currency:
    id: int
    name: str
    code: str
    sign: str
