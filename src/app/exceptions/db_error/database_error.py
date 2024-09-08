from src.app.exceptions.user_error import UserError


class DataBaseError(UserError):
    def __init__(self, message: str):
        super().__init__(message, 500)
