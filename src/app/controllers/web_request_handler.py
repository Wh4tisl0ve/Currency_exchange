from http.server import BaseHTTPRequestHandler
import urllib.parse


class WebRequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, code, content_type='text/html', body=b''):
        self.send_response(code)
        self.send_header(content_type, content_type)
        self.end_headers()
        self.wfile.write(body.encode('utf-8'))

    def do_GET(self):
        if self.path == '/':
            self._send_response(200, 'text/html', '<h1>Hello, GET!</h1>')
        elif self.path.startswith('/currencies'):
            o = urllib.parse.urlparse(self.path).query
            print(urllib.parse.parse_qs(o))
            self._send_response(200, 'text/html', '<h1>currencies</h1>')
        else:
            self._send_response(404, 'text/html', '<h1>404 Not Found</h1>')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self._send_response(200, 'application/json', post_data)
