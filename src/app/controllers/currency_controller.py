import json
from src.app.database.db_client import DBClient
from src.app.dto.currency_dto import CurrencyDTO
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
            currency = self.__service.get_concrete_currency(currency_code)
            return json.dumps(currency.to_dict(), indent=4)

        @self.__router.route('/currencies', method='POST')
        def add_currency(request: dict):
            request_dto = CurrencyDTO(name=request.get('name'),
                                      code=request.get('code'),
                                      sign=request.get('sign'))

            added_currency = self.__service.add_currency(request_dto)
            return json.dumps(added_currency.to_dict(), indent=4)
