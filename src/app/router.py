from src.app.exceptions.not_found_error import NotFoundError
from typing import Callable
import re


class Router:
    __routes = {'GET': {}, 'POST': {}, 'PATCH': {}}
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Router, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def route(self, path: str, method: str = 'GET') -> Callable:
        def register_routes(handler: Callable) -> Callable:
            self.__routes[method][re.compile(path)] = handler
            return handler

        return register_routes

    def resolve(self, path: str, method: str = 'GET') -> tuple[Callable, dict]:
        for url, handler in self.__routes[method].items():
            match = url.match(path)
            if match:
                return handler, match.groupdict()

        raise NotFoundError('Endpoint not found')
