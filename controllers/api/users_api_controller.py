from controllers.api.api_controller import ApiController
from exceptions import InvalidArgumentException
from models.user import User
from models.user_auth_service import UserAuthService


class UsersApiController(ApiController):

    def user(self, request, response):
        response.json = {
            "user": self.user.get_nickname() if self.user else "No authenticated"
        }

    def login(self, request, response):
        try:
            data = request.json_body
            if not isinstance(data, dict):
                raise InvalidArgumentException("Нужен объект JSON")
            user = User.sign_in(data)
        except (InvalidArgumentException, KeyError, ValueError, TypeError) as exc:
            response.status_code = 401
            response.json = {
                "user": "No authenticated",
                "error": str(exc) or "Неверный логин или пароль",
            }
            return

        token = UserAuthService.create_token(user)
        response.set_cookie(
            "token", token, max_age=500, path="/",
            httponly=True, secure=(request.scheme == "https"), samesite="Lax",
        )
        response.json = {"user": user.get_nickname()}
