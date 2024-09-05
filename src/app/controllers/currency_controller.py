import json
from src.app.database.db_client import DBClient
from src.app.dto.currency_dto import CurrencyDTO
from src.app.exceptions.currency_error.currency_already_exists import CurrencyAlreadyExists
from src.app.exceptions.currency_error.currency_not_found_error import CurrencyNotFoundError
from src.app.router.router import Router
from src.app.services.currency_service import CurrencyService


class CurrencyController:
    def __init__(self, db_client: DBClient, router: Router):
        self.__service = CurrencyService(db_client)
        self.__router = router
        self.register_routes()

    def register_routes(self):
        @self.__router.route('/currencies', method='GET')
        def get_all_currencies() -> json:
            currencies = self.__service.get_all_currencies()
            return json.dumps([currency.to_dict() for currency in currencies], indent=4)

        @self.__router.route(r'^/currency/(?P<currency_code>[a-zA-Z]{3})$', method='GET')
        def get_concrete_currencies(currency_code: str):
            try:
                currency = self.__service.get_concrete_currency(currency_code)
            except CurrencyNotFoundError as currency_not_found:
                return json.dumps(currency_not_found.to_dict(), indent=4)

            return json.dumps(currency.to_dict(), indent=4)

        @self.__router.route('/currencies', method='POST')
        def add_currency(request: dict):
            request_dto = CurrencyDTO(name=request.get('name'),
                                      code=request.get('code'),
                                      sign=request.get('sign'))
            try:
                added_currency = self.__service.add_currency(request_dto)
            except CurrencyAlreadyExists as currency_exists:
                return json.dumps(currency_exists.to_dict(), indent=4)

            return json.dumps(added_currency.to_dict(), indent=4)
