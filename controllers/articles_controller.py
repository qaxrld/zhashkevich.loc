
from controllers.controller import Controller
from models.article import Article
from services.db import Db

class ArticlesController(Controller):

    def index(self, request, response):
        articles = Article.find_all(Article)
        print(articles)
        response.text = self.view.render_html('articles/index.html', {'title' : 'Статьи',
                                                                    'h1' : 'Статьи на сайте', 'articles' : articles})


    def view(self, request, response, id):
        article = Article.get_by_id(id, Article)
        response.text = self.view.render_html('articles/view.html', {'title' : f'MVC фреймворк - {article.name}', 'h1' : f'Статья: {article.name} ', 'article' : article})
