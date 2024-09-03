from src.app.dao.currencies_dao import CurrenciesDAO
from src.app.database.db_client import DBClient
from src.app.mappers.currency_mapper import CurrencyMapper
from src.app.router.router import Router
from src.app.services.currency_service import CurrencyService


class CurrencyController:
    def __init__(self, db_client: DBClient, router: Router):
        self.__dao = CurrenciesDAO(db_client)
        self.__mapper = CurrencyMapper()
        self.__service = CurrencyService(self.__dao, self.__mapper)
        self.__router = router
        self.register_routes()

    def register_routes(self):
        @self.__router.route('/currencies', method='GET')
        def get_all_currencies():
            print(self.__service.get_all_currencies())

    """def do_GET(self):
        if self.path == '/':
            self._send_response(200, 'text/html', '<h1>Hello, GET!</h1>')
        elif self.path.startswith('/currencies'):
            o = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(o.query)
            print(query_params)
            self._send_response(200, 'text/html', '<h1>currencies</h1>')
"""
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self._send_response(200, 'application/json', post_data)
