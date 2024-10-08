from src.app.controllers import currency_controller, exchanger_controller, exchange_rate_controller
from src.db_scripts.create_database import create_database
from src.app.request_handler import RequestHandler
from http.server import HTTPServer


def run_server(server_class=HTTPServer, handler_class=RequestHandler, port=8080) -> None:
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server running on port {port}')
    httpd.serve_forever()


def main() -> None:
    create_database()
    run_server()


if __name__ == "__main__":
    main()
