import re


class Router:
    def __init__(self):
        self.routes = {'GET': {}, 'POST': {}, 'PATCH': {}}

    def route(self, path: str, method='GET'):
        def wrapper(handler):
            self.routes[method][path] = handler
            return handler

        return wrapper

    def resolve(self, path, method='GET'):
        params = self.split_url(path)
        handler = self.routes.get(method).get(f'/{params[0]}')
        if handler:
            return handler(params[1])
        else:
            return self.not_found()

    def split_url(self, url: str):
        pattern = r'^/([^/]+)/([^/]+)$'
        match = re.match(pattern, url)
        subpaths = match.groups()
        if subpaths:
            return subpaths
        else:
            return url

    def not_found(self) -> str:
        # возврат html template страницы
        return '<h1>404 Not found</h1>'
