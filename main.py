from http.server import HTTPServer

from src.web_request_handler import WebRequestHandler


def main():
    host = '127.0.0.1'
    port = 8000
    server_address = (host, port)
    httpd = HTTPServer(server_address, WebRequestHandler)
    print(f'Запущен на {port} порту...')
    httpd.serve_forever()


if __name__ == '__main__':
    main()
