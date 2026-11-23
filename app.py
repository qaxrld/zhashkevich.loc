import re

from webob import Request, Response
from whitenoise import WhiteNoise

import routes
from exceptions import (
    ForbiddenException,
    InvalidArgumentException,
    InvalidMethodException,
    NotFoundException,
    UnauthorizedException,
)
from views.view import View


class API:
    def __init__(self, static_dir="assets"):
        self.routes = routes.routes
        self.whitenoise = WhiteNoise(self.wsgi_app, root=static_dir)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.whitenoise(environ, start_response)

    def handle_request(self, request):
        response = Response()
        is_api = request.path.startswith("/api/")

        try:
            result = self.find_handler_re(request_path=request.path)
            if result is None:
                raise NotFoundException("Страница не найдена")

            handler, params = result
            controller = handler[0](request)

            if isinstance(handler[1], dict):
                action = handler[1].get(request.method)
                if action is None:
                    raise InvalidMethodException("Метод не поддерживается")
            else:
                action = handler[1]

            action(controller, request, response, *params)

        except NotFoundException as exc:
            response.status_code = 404
            if is_api:
                response.json = {"error": str(exc)}
            else:
                response.text = View("default").render_html(
                    "errors/404.html", {"error": exc}
                )
        except UnauthorizedException as exc:
            response.status_code = 401
            if is_api:
                response.headers["WWW-Authenticate"] = 'Basic realm="Articles API"'
                response.json = {"error": str(exc)}
            else:
                response.text = View("default").render_html(
                    "errors/401.html", {"error": exc}
                )
        except ForbiddenException as exc:
            response.status_code = 403
            response.json = {"error": str(exc)}
        except InvalidMethodException as exc:
            response.status_code = 405
            response.json = {"error": str(exc)}
        except InvalidArgumentException as exc:
            response.status_code = 400
            response.json = {"error": str(exc)}

        return response

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            if path == request_path:
                return handler

    def find_handler_re(self, request_path):
        for path, handler in self.routes.items():
            match = re.search(path, request_path)
            if match is not None:
                return handler, match.groups()

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found"

    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper


app = API()
