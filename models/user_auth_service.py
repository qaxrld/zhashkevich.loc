import base64
import binascii

from werkzeug.security import check_password_hash

from models.user import User


class UserAuthService:

    @staticmethod
    def create_token(user):
        return str(user.get_id()) + ":" + user.get_auth_token()

    @staticmethod
    def get_user_by_token(token):
        if not token:
            return None
        try:
            user_id, auth_token = token.split(":", 1)
            user = User.get_by_id(int(user_id))
        except (TypeError, ValueError):
            return None
        if user is None or user.get_auth_token() != auth_token:
            return None
        return user

    @staticmethod
    def get_user_by_auth_basic(request):
        header = request.headers.get("Authorization", "")
        kind, separator, encoded = header.partition(" ")
        if not separator or kind.lower() != "basic":
            return None
        try:
            decoded = base64.b64decode(
                encoded.strip(), validate=True
            ).decode("utf-8")
            nickname, password = decoded.split(":", 1)
        except (ValueError, UnicodeDecodeError, binascii.Error):
            return None

        if not nickname or not password:
            return None
        user = User.find_one_by_column("nickname", nickname)
        if user is None:
            return None
        if not check_password_hash(user.get_password_hash(), password):
            return None
        return user
