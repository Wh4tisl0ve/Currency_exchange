from http.server import BaseHTTPRequestHandler
import urllib.parse

from src.app.controllers.base_controller import BaseController


class CurrencyController(BaseController):

    #@app.route('/currencies', methods=['GET'])
    def do_GET(self):
        if self.path == '/':
            self._send_response(200, 'text/html', '<h1>Hello, GET!</h1>')
        elif self.path.startswith('/currencies'):
            o = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(o.query)
            print(query_params)
            self._send_response(200, 'text/html', '<h1>currencies</h1>')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self._send_response(200, 'application/json', post_data)
