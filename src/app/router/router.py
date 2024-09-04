import re


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

        # exception
        return self.not_found()

    def not_found(self) -> str:
        # возврат html template страницы
        return '<h1>404 Not found</h1>'
