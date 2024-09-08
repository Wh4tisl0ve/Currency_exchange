from src.app.controllers.request_handler import RequestHandler
from src.app.controllers.controllers import create_controllers
from src.app.db_clients.sqlite_client import SQLiteClient
from src.app.db_clients.config.config import load_config
from http.server import HTTPServer


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080) -> None:
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


def main() -> None:
    config = load_config()
    sqlite_client = SQLiteClient(config)
    create_controllers(sqlite_client)
    run()


if __name__ == "__main__":
    main()
