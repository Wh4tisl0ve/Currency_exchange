import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from src.app.controllers.currency_controller import CurrencyController
from src.app.controllers.request_handler import RequestHandler
from src.app.database.sqlite_client import SQLiteClient


current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
with open(os.path.join(current_dir, 'database', 'config', 'config.json'), 'r', encoding='utf-8') as f:
    config = json.load(f)

db_client = SQLiteClient(config)
router = RequestHandler.router
home_controller = CurrencyController(db_client, router)


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()


run()
