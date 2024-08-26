from http.server import BaseHTTPRequestHandler


class WebRequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, code, content_type='text/html', body=b''):
        self.send_response(code)
        self.send_header(content_type, content_type)
        self.end_headers()
        self.wfile.write(body.encode('utf-8'))

    def do_GET(self):
        if self.path == '/':
            self._send_response(200, 'text/html', '<h1>Hello, GET!</h1>')

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)

        self._send_response(200)
        response = f"Received POST data: {data.decode('utf-8')}"
        self.wfile.write(response.encode('utf-8'))
