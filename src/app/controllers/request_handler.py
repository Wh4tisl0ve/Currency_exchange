from urllib.parse import parse_qs, urlparse

from src.app.router.router import Router
from http.server import BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):
    router = Router()

    def do_GET(self):
        handler, params = self.router.resolve(self.path, method='GET')
        query_params = parse_qs(urlparse(self.path).query)
        if query_params:
            query_params = {k: v[0] for k, v in query_params.items()}
            params = query_params
            response = handler(params)
        else:
            response = handler(**params)
        self._send_response(200, 'application/json', response)

    def do_POST(self):
        params = self.get_post_data()

        handler = self.router.resolve(self.path, method='POST')[0]
        response = handler(params)

        self._send_response(200, 'application/json', response)

    def do_PATCH(self):
        params = self.get_post_data()
        params['path'] = self.path

        try:
            handler = self.router.resolve(self.path, method='PATCH')[0]
            response = handler(params)
            self._send_response(200, 'application/json', response)
        except Exception:
            self._send_response(404, 'text/html', '<h1>404 Not found</h1>')

    def get_post_data(self) -> dict:
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        params = parse_qs(post_data.decode('utf-8'))
        params = {k: v[0] for k, v in params.items()}
        return params

    def _send_response(self, code, content_type, body):
        self.send_response(code)
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(body.encode('utf-8'))

