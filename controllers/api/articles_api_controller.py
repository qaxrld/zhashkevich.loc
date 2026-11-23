
from controllers.controller import Controller
from models.article import Article
from exceptions import NotFoundException


class ArticlesApiController(Controller):

    def view(self, request, response, id):
        article = Article.get_by_id(int(id))

        if article is None:
            raise NotFoundException("Статья не найдена")

        data = {
            "id": article.get_id(),
            "name": article.get_name(),
            "text": article.get_text(),
            "author_id": article.get_author_id()
        }

        response.content_type = "application/json"
        response.text = self.view.display_json(data)

    def index(self, request, response):
        articles = Article.find_all()

        data = []

        for article in articles:
            data.append({
                "id": article.get_id(),
                "name": article.get_name(),
                "text": article.get_text(),
                "author_id": article.get_author_id()
            })

        response.content_type = "application/json"
        response.text = self.view.display_json(data)
