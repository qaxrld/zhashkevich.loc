from controllers.controller import Controller
from models.user_auth_service import UserAuthService


class ApiController(Controller):
    def __init__(self, request):
        super().__init__(request)
        # For API writes, only valid HTTP Basic credentials count.
        self.user = UserAuthService.get_user_by_auth_basic(request)
