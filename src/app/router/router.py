import re
from src.app.exceptions.endpoint_not_found_error import EndpointNotFoundError


class Router:
    def __init__(self):
        self.routes = {'GET': {}, 'POST': {}, 'PATCH': {}}

    def route(self, path: str, method: str = 'GET'):
        def register_routes(handler):
            self.routes[method][re.compile(path)] = handler
            return handler

        return register_routes

    def resolve(self, path: str, method: str = 'GET'):
        for url, handler in self.routes[method].items():
            match = url.match(path)
            if match:
                return handler, match.groupdict()

        raise EndpointNotFoundError('Эндпоинт не найден', 404)
