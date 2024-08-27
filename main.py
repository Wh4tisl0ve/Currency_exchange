import json
from http.server import HTTPServer

from src.Database.sqlite_client import SQLiteClient
from src.web_request_handler import WebRequestHandler


def main():
    host = '127.0.0.1'
    port = 8000
    server_address = (host, port)
    httpd = HTTPServer(server_address, WebRequestHandler)
    # Opening JSON file
    f = open('src/database/config/config.json')
    ditc = json.load(f)
    SQLiteClient(ditc).open_connection()


if __name__ == '__main__':
    main()
