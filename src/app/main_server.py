import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from src.app.controllers.currency_controller import CurrencyController
from src.app.controllers.exchange_rates_controller import ExchangeRatesController
from src.app.controllers.exchanger_controller import ExchangerController
from src.app.controllers.request_handler import RequestHandler
from src.app.db_clients.sqlite_client import SQLiteClient


current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
with open(os.path.join(current_dir, 'db_clients', 'config', 'config.json'), 'r', encoding='utf-8') as f:
    config = json.load(f)

db_client = SQLiteClient(config)
router = RequestHandler.router
currency_controller = CurrencyController(db_client, router)
exchange_rates_controller = ExchangeRatesController(db_client, router)
exchanger_controller = ExchangerController(db_client, router)


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()


run()
