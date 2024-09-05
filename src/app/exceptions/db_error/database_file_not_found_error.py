from src.app.exceptions.db_error.database_error import DataBaseError
from src.app.exceptions.not_found_error import NotFoundError


class DatabaseFileNotFoundError(DataBaseError, NotFoundError):
    pass
