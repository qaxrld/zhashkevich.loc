"""Проверки REST API практической работы № 7.

Запуск: python -m unittest discover -s tests -v
Тесты не изменяют настоящую базу данных.
"""

import base64
import unittest
from unittest.mock import Mock, patch

from webob import Request

from app import app
from models.article import Article
from models.user import User
from models.user_auth_service import UserAuthService
from werkzeug.security import generate_password_hash


def request(method, url, data=None, headers=None):
    import json
    kwargs = {"method": method, "headers": headers or {}}
    if data is not None:
        kwargs["body"] = json.dumps(data).encode("utf-8")
        kwargs["content_type"] = "application/json"
    return Request.blank(url, **kwargs)


def fake_article(author_id=1, article_id=12):
    article = Mock()
    article.get_id.return_value = article_id
    article.get_name.return_value = "Тестовая статья"
    article.get_text.return_value = "Текст статьи"
    article.get_author_id.return_value = author_id
    return article


def fake_user(user_id=1):
    user = Mock()
    user.get_id.return_value = user_id
    user.get_nickname.return_value = "testapi2026"
    return user


class ArticlesApiTests(unittest.TestCase):

    def test_get_one_article(self):
        with patch.object(Article, "get_by_id", return_value=fake_article()):
            response = app.handle_request(request("GET", "/api/article/12"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Тестовая статья")

    def test_get_all_articles(self):
        with patch.object(Article, "find_all", return_value=[fake_article()]):
            response = app.handle_request(request("GET", "/api/articles/"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_post_without_auth_returns_401(self):
        response = app.handle_request(
            request("POST", "/api/articles/", {"name": "Тест", "text": "Текст"})
        )
        self.assertEqual(response.status_code, 401)

    def test_post_with_auth_creates_article(self):
        with patch.object(UserAuthService, "get_user_by_auth_basic", return_value=fake_user()):
            with patch.object(Article, "save"):
                response = app.handle_request(
                    request("POST", "/api/articles/",
                            {"name": "Название", "text": "Текст"})
                )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["article"]["author_id"], 1)

    def test_put_updates_own_article(self):
        article = fake_article()
        with patch.object(UserAuthService, "get_user_by_auth_basic", return_value=fake_user()):
            with patch.object(Article, "get_by_id", return_value=article):
                response = app.handle_request(
                    request("PUT", "/api/articles/12", {"name": "Новое название"})
                )
        self.assertEqual(response.status_code, 200)
        article.set_name.assert_called_once_with("Новое название")
        article.save.assert_called_once()

    def test_put_other_users_article_returns_403(self):
        article = fake_article(author_id=2)
        with patch.object(UserAuthService, "get_user_by_auth_basic", return_value=fake_user()):
            with patch.object(Article, "get_by_id", return_value=article):
                response = app.handle_request(
                    request("PUT", "/api/articles/12", {"name": "Чужая"})
                )
        self.assertEqual(response.status_code, 403)
        article.save.assert_not_called()

    def test_delete_own_article(self):
        article = fake_article()
        with patch.object(UserAuthService, "get_user_by_auth_basic", return_value=fake_user()):
            with patch.object(Article, "get_by_id", return_value=article):
                response = app.handle_request(request("DELETE", "/api/articles/12"))
        self.assertEqual(response.status_code, 200)
        article.delete.assert_called_once()

    def test_delete_other_users_article_returns_403(self):
        article = fake_article(author_id=2)
        with patch.object(UserAuthService, "get_user_by_auth_basic", return_value=fake_user()):
            with patch.object(Article, "get_by_id", return_value=article):
                response = app.handle_request(request("DELETE", "/api/articles/12"))
        self.assertEqual(response.status_code, 403)
        article.delete.assert_not_called()

    def test_unsupported_method_returns_405(self):
        response = app.handle_request(request("PATCH", "/api/articles/"))
        self.assertEqual(response.status_code, 405)

    def test_missing_article_returns_404(self):
        with patch.object(Article, "get_by_id", return_value=None):
            response = app.handle_request(request("GET", "/api/article/999999"))
        self.assertEqual(response.status_code, 404)

    def test_get_api_user_without_login(self):
        response = app.handle_request(request("GET", "/api/user"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["user"], "No authenticated")

    def test_invalid_basic_auth(self):
        encoded = base64.b64encode(b"testapi2026:wrong").decode("ascii")
        fake = fake_user()
        fake.get_password_hash.return_value = generate_password_hash(
            "right-password", method="pbkdf2:sha256"
        )
        with patch.object(User, "find_one_by_column", return_value=fake):
            result = UserAuthService.get_user_by_auth_basic(
                request("GET", "/api/user", headers={"Authorization": "Basic " + encoded})
            )
        self.assertIsNone(result)

    def test_valid_basic_auth(self):
        encoded = base64.b64encode(b"testapi2026:right-password").decode("ascii")
        fake = fake_user()
        fake.get_password_hash.return_value = generate_password_hash(
            "right-password", method="pbkdf2:sha256"
        )
        with patch.object(User, "find_one_by_column", return_value=fake):
            result = UserAuthService.get_user_by_auth_basic(
                request("GET", "/api/user", headers={"Authorization": "Basic " + encoded})
            )
        self.assertIs(result, fake)


if __name__ == "__main__":
    unittest.main()
