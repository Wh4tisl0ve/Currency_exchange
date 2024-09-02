from http.server import HTTPServer

from src.app.controllers.currency_controller import CurrencyController


def main():
    server = HTTPServer(('', 8000), CurrencyController)
    server.serve_forever()



if __name__ == '__main__':
    main()
