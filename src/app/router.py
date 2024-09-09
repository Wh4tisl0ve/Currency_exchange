from src.app.exceptions.not_found_error import NotFoundError
from src.app.db_clients.singleton import Singleton
from typing import Callable
import re


class Router(metaclass=Singleton):
    def __init__(self):
        self.routes = {'GET': {}, 'POST': {}, 'PATCH': {}}

    def route(self, path: str, method: str = 'GET') -> Callable:
        def register_routes(handler: Callable) -> Callable:
            self.routes[method][re.compile(path)] = handler
            return handler

        return register_routes

    def resolve(self, path: str, method: str = 'GET') -> tuple[Callable, dict]:
        for url, handler in self.routes[method].items():
            match = url.match(path)
            if match:
                return handler, match.groupdict()

        raise NotFoundError('Эндпоинт не найден')
