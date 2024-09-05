class CurrencyAlreadyExists(Exception):
    def __init__(self, message: str, code: int):
        super().__init__(message)
        self.__code = code

    def to_dict(self) -> dict:
        return {"message": self.args[0],
                "code": self.__code}