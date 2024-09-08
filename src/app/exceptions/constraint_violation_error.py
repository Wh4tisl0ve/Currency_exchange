from src.app.exceptions.user_error import UserError


class ConstraintViolationException(UserError):
    def __init__(self, message: str):
        super().__init__(message, 409)