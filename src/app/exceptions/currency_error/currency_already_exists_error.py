from src.app.exceptions.constraint_violation_error import ConstraintViolationException


class CurrencyAlreadyExists(ConstraintViolationException):
    pass