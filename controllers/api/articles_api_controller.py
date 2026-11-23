from controllers.api.api_controller import ApiController
from exceptions import (
    ForbiddenException,
    InvalidArgumentException,
    NotFoundException,
    UnauthorizedException,
)
from models.article import Article


class ArticlesApiController(ApiController):

    @staticmethod
    def article_data(article):
        return {
            "id": article.get_id(),
            "name": article.get_name(),
            "text": article.get_text(),
            "author_id": article.get_author_id(),
        }

    @staticmethod
    def body_data(request):
        try:
            data = request.json_body
        except (ValueError, TypeError) as exc:
            raise InvalidArgumentException("Нужен корректный JSON") from exc
        if not isinstance(data, dict):
            raise InvalidArgumentException("Нужен объект JSON")
        return data

    def require_user(self):
        if self.user is None:
            raise UnauthorizedException("Сначала войдите")

    def require_author(self, article):
        self.require_user()
        if str(article.get_author_id()) != str(self.user.get_id()):
            raise ForbiddenException("Это не ваша статья")

    def view(self, request, response, id):
        article = Article.get_by_id(int(id))
        if article is None:
            raise NotFoundException("Статья не найдена")
        response.json = self.article_data(article)

    def index(self, request, response):
        response.json = [
            self.article_data(article) for article in Article.find_all()
        ]

    def add(self, request, response):
        self.require_user()
        data = self.body_data(request)
        name = str(data.get("name") or "").strip()
        text = str(data.get("text") or "").strip()
        if not name or not text:
            raise InvalidArgumentException("Заполните название и текст")

        article = Article()
        article.set_name(name)
        article.set_text(text)
        article.set_author_id(self.user.get_id())
        article.save()

        response.status_code = 201
        response.json = {"message": "Статья добавлена"}

    def edit(self, request, response, id):
        self.require_user()
        article = Article.get_by_id(int(id))
        if article is None:
            raise NotFoundException("Статья не найдена")
        self.require_author(article)
        data = self.body_data(request)

        if "name" in data:
            name = str(data["name"] or "").strip()
            if not name:
                raise InvalidArgumentException("Название не может быть пустым")
            article.set_name(name)
        if "text" in data:
            text = str(data["text"] or "").strip()
            if not text:
                raise InvalidArgumentException("Текст не может быть пустым")
            article.set_text(text)

        article.save()
        response.json = {
            "message": "Статья изменена",
            "article": self.article_data(article),
        }

    def delete(self, request, response, id):
        self.require_user()
        article = Article.get_by_id(int(id))
        if article is None:
            raise NotFoundException("Статья не найдена")
        self.require_author(article)
        article.delete()
        response.json = {"message": "Статья удалена"}
