from abc import ABC, abstractmethod
from http.server import BaseHTTPRequestHandler


class BaseController(BaseHTTPRequestHandler):
    @abstractmethod
    def do_GET(self):
        pass

    @abstractmethod
    def do_POST(self):
        pass

    @abstractmethod
    def do_PATCH(self):
        pass

    def _send_response(self, code, content_type, body):
        self.send_response(code)
        self.send_header(content_type, content_type)
        self.end_headers()
        self.wfile.write(body.encode('utf-8'))
