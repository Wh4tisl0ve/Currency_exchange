from src.app.exceptions.currency_error.currency_not_found_error import CurrencyNotFoundError
from src.app.exceptions.currency_error.currency_already_exists_error import CurrencyAlreadyExists
from src.app.exceptions.required_field_missing_error import RequiredFieldMissingError
from src.app.exceptions.no_content_error import NoContentError
from src.app.services.currency_service import CurrencyService
from src.app.database.db_client import DBClient
from src.app.dto.currency_dto import CurrencyDTO
from src.app.router.router import Router


class CurrencyController:
    def __init__(self, db_client: DBClient, router: Router):
        self.__service = CurrencyService(db_client)
        self.__router = router
        self.register_routes()

    def register_routes(self):
        @self.__router.route(r'^/currencies$', method='GET')
        def get_all_currencies() -> dict:
            try:
                currencies = self.__service.get_all_currencies()
            except NoContentError as no_content:
                return no_content.to_dict()

            return {"code": 200, "body": [currency.to_dict() for currency in currencies]}

        @self.__router.route(r'^/currency/(?P<currency_code>[a-zA-Z]{3})$', method='GET')
        def get_concrete_currencies(currency_code: str) -> dict:
            try:
                currency = self.__service.get_concrete_currency(currency_code)
            except CurrencyNotFoundError as currency_not_found:
                return currency_not_found.to_dict()

            return {"code": 200, "body": currency.to_dict()}

        @self.__router.route(r'^/currencies$', method='POST')
        def add_currency(request: dict) -> dict:
            try:
                request_dto = CurrencyDTO(name=request['name'],
                                          code=request['code'],
                                          sign=request['sign'])
                added_currency = self.__service.add_currency(request_dto)
            except KeyError:
                field_missing = RequiredFieldMissingError('Отсутствует нужное поле формы', 400)
                return field_missing.to_dict()
            except CurrencyAlreadyExists as currency_exists:
                return currency_exists.to_dict()

            return {"code": 201, "body": added_currency.to_dict()}