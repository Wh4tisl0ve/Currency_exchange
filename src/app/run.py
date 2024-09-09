from src.app.controllers.currency_controller import CurrencyController
from src.app.controllers.exchange_rate_controller import ExchangeRateController
from src.app.controllers.exchanger_controller import ExchangerController
from src.app.dao.currency_dao import CurrencyDAO
from src.app.dao.exchange_rate_dao import ExchangeRateDAO
from src.app.request_handler import RequestHandler
from http.server import HTTPServer

from src.app.services.currency_service import CurrencyService
from src.app.services.exchange_rate_service import ExchangeRateService
from src.app.services.exchanger_service import ExchangerService


def run_server(server_class=HTTPServer, handler_class=RequestHandler, port=8080) -> None:
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server is started in {port}')
    httpd.serve_forever()


def main() -> None:
    currency_dao = CurrencyDAO()
    exchange_rates_dao = ExchangeRateDAO()

    currency_service = CurrencyService(currency_dao)
    exchange_rates_service = ExchangeRateService(exchange_rates_dao)
    exchanger_service = ExchangerService(exchange_rates_dao, currency_dao)

    CurrencyController(currency_service)
    ExchangeRateController(exchange_rates_service, currency_service)
    ExchangerController(exchanger_service, currency_service)

    run_server()


if __name__ == "__main__":
    main()
