from urllib.parse import parse_qs

from src.app.router.router import Router
from http.server import BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):
    router = Router()

    def do_GET(self):
        try:
            handler, params = self.router.resolve(self.path, method='GET')
            response = handler(**params)
            self._send_response(200, 'application/json', response)
        except Exception:
            self._send_response(404, 'text/html', '<h1>404 Not found</h1>')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        params = parse_qs(post_data.decode('utf-8'))
        params = {k: v[0] for k, v in params.items()}
        try:
            handler = self.router.resolve(self.path, method='POST')[0]
            response = handler(params)
            self._send_response(200, 'application/json', response)
        except Exception:
            self._send_response(404, 'text/html', '<h1>404 Not found</h1>')

    def do_PATCH(self):
        pass

    def _send_response(self, code, content_type, body):
        self.send_response(code)
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(body.encode('utf-8'))
