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
        pass

    def do_PATCH(self):
        pass

    def _send_response(self, code, content_type, body):
        self.send_response(code)
        self.send_header(content_type, content_type)
        self.end_headers()
        self.wfile.write(body.encode('utf-8'))
