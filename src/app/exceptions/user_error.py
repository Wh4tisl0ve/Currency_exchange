class UserError(Exception):
    def __init__(self, message: str, code: int):
        super().__init__(message)
        self.__code = code

    def to_dict(self) -> dict:
        return {"body": {"error": self.args[0]},
                "code": self.__code}
