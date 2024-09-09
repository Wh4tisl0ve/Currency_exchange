from src.app.exceptions.endpoint_not_found_error import EndpointNotFoundError
from src.app.exceptions.db_error.database_error import DataBaseError
from src.app.router import Router
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from sqlite3 import OperationalError
import json


class RequestHandler(BaseHTTPRequestHandler):
    router = Router()

    def do_GET(self) -> None:
        try:
            handler, params = self.router.resolve(urlparse(self.path).path, method='GET')
            query_params = parse_qs(urlparse(self.path).query)

            if query_params:
                query_params = {k: v[0] for k, v in query_params.items()}
                params = query_params
                response = handler(params)
            else:
                response = handler(**params)
        except (DataBaseError, EndpointNotFoundError) as e:
            response = e.to_dict()
        except OperationalError:
            response = DataBaseError('Нет доступа к базе данных').to_dict()

        self.__send_response(response['code'], 'application/json', json.dumps(response['body'], indent=4))

    def do_POST(self) -> None:
        params = self.get_params()
        try:
            handler = self.router.resolve(self.path, method='POST')[0]
            response = handler(params)
        except (DataBaseError, EndpointNotFoundError) as e:
            response = e.to_dict()
        except OperationalError:
            response = DataBaseError('Нет доступа к базе данных').to_dict()

        self.__send_response(response['code'], 'application/json', json.dumps(response['body'], indent=4))

    def do_PATCH(self) -> None:
        params = self.get_params()
        params['path'] = self.path

        try:
            handler = self.router.resolve(self.path, method='PATCH')[0]
            response = handler(params)
        except (DataBaseError, EndpointNotFoundError) as e:
            response = e.to_dict()
        except OperationalError:
            e = DataBaseError('Нет доступа к базе данных')
            response = e.to_dict()

        self.__send_response(response['code'], 'application/json', json.dumps(response['body'], indent=4))

    def get_params(self) -> dict:
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        params = parse_qs(post_data.decode('utf-8'))
        params = {k: v[0] for k, v in params.items()}
        return params

    def __send_response(self, code, content_type, body) -> None:
        self.send_response(code)
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(body.encode('utf-8'))
