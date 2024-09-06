from src.app.exceptions.constraint_violation_exception import ConstraintViolationException


class ExchangeRateAlreadyExists(ConstraintViolationException):
    pass