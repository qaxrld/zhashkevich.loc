"""Проверка прав владельца для обычных HTML-маршрутов."""

import unittest
from unittest.mock import Mock, patch
from webob import Request

from app import app
from models.article import Article
from models.user_auth_service import UserAuthService


def make_article(author_id):
    obj = Mock()
    obj.get_id.return_value = 12
    obj.get_author_id.return_value = author_id
    return obj


def make_user(user_id):
    obj = Mock()
    obj.get_id.return_value = user_id
    return obj


def request(method, url):
    return Request.blank(url, method=method, headers={"Cookie": "token=test"})


class IdorTests(unittest.TestCase):
    def test_get_edit_other_users_article_returns_403(self):
        with patch.object(UserAuthService, "get_user_by_token", return_value=make_user(1)):
            with patch.object(Article, "get_by_id", return_value=make_article(2)):
                result = app.handle_request(request("GET", "/article/12/edit"))
        self.assertEqual(result.status_code, 403)

    def test_post_edit_other_users_article_returns_403(self):
        article = make_article(2)
        with patch.object(UserAuthService, "get_user_by_token", return_value=make_user(1)):
            with patch.object(Article, "get_by_id", return_value=article):
                result = app.handle_request(request("POST", "/article/12/edit"))
        self.assertEqual(result.status_code, 403)
        article.save.assert_not_called()

    def test_post_delete_other_users_article_returns_403(self):
        article = make_article(2)
        with patch.object(UserAuthService, "get_user_by_token", return_value=make_user(1)):
            with patch.object(Article, "get_by_id", return_value=article):
                result = app.handle_request(request("POST", "/article/12/delete"))
        self.assertEqual(result.status_code, 403)
        article.delete.assert_not_called()

    def test_post_delete_without_login_returns_401(self):
        article = make_article(2)
        with patch.object(UserAuthService, "get_user_by_token", return_value=None):
            with patch.object(Article, "get_by_id", return_value=article):
                result = app.handle_request(request("POST", "/article/12/delete"))
        self.assertEqual(result.status_code, 401)
        article.delete.assert_not_called()

    def test_delete_get_returns_405(self):
        result = app.handle_request(request("GET", "/article/12/delete"))
        self.assertEqual(result.status_code, 405)

    def test_owner_can_delete(self):
        article = make_article(1)
        with patch.object(UserAuthService, "get_user_by_token", return_value=make_user(1)):
            with patch.object(Article, "get_by_id", return_value=article):
                result = app.handle_request(request("POST", "/article/12/delete"))
        self.assertEqual(result.status_code, 302)
        article.delete.assert_called_once()


if __name__ == "__main__":
    unittest.main()
