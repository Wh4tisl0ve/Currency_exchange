from http.server import HTTPServer,  SimpleHTTPRequestHandler


class WebRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello, w')

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = f"Received POST data: {data.decode('utf-8')}"
        self.wfile.write(response.encode('utf-8'))


host = '127.0.0.1'
port = 8000

server_address = (host, port)
httpd = HTTPServer(server_address, WebRequestHandler)
try:
    print(f'Запущен на порту {port}')
    httpd.serve_forever()
except Exception:
    httpd.shutdown()
