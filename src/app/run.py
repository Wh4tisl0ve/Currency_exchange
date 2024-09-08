from src.app.request_handler import RequestHandler
from src.app.controllers.controllers import create_controllers
from src.app.db_clients.sqlite_client import SQLiteClient
from src.app.router import Router
from http.server import HTTPServer


def run_server(server_class=HTTPServer, handler_class=RequestHandler, port=8080) -> None:
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server is started in {port}')
    httpd.serve_forever()


def main() -> None:
    SQLiteClient().open_connection()
    Router()
    create_controllers()
    run_server()


if __name__ == "__main__":
    main()
