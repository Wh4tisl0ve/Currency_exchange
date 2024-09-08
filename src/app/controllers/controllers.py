from src.app.controllers.exchange_rates_controller import ExchangeRatesController
from src.app.controllers.exchanger_controller import ExchangerController
from src.app.controllers.currency_controller import CurrencyController
from src.app.controllers.request_handler import RequestHandler
from src.app.db_clients.db_client import DBClient


def create_controllers(db_client: DBClient) -> None:
    router = RequestHandler.router
    CurrencyController(db_client, router),
    ExchangeRatesController(db_client, router),
    ExchangerController(db_client, router)