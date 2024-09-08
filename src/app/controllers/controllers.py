from src.app.controllers.exchange_rates_controller import ExchangeRatesController
from src.app.controllers.exchanger_controller import ExchangerController
from src.app.controllers.currency_controller import CurrencyController


def create_controllers() -> None:
    CurrencyController(),
    ExchangeRatesController(),
    ExchangerController()
