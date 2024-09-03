class Router:
    def __init__(self):
        self.routes = {}

    def route(self, path: str, method='GET'):
        def wrapper(handler):
            self.routes[method] = {path: handler}
            return handler

        return wrapper

    def resolve(self, path, method='GET'):
        handler = self.routes.get(method).get(path)
        if handler:
            return handler
        else:
            return self.not_found()

    def not_found(self) -> str:
        return '<h1>404 Not found</h1>'
