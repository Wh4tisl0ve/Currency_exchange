from dataclasses import dataclass


@dataclass(frozen=True)
class Currency:
    id: int
    name: str
    code: str
    sign: str

    def to_dict(self):
        return self.to_dict()
