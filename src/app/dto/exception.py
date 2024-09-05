from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class ExceptionDTO:
    message: str = 'Возникло исключение'
    code: int = 404

    def to_dict(self) -> dict:
        return asdict(self)