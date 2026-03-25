
from controllers.controller import Controller
from models.articles import Articles
from services.db import Db

class ArticlesController(Controller):

    def index(self, request, response):
        articles = Articles.findAll()
        print(articles)
        response.text = self.view.render_html('articles/index.html', {'title' : 'Статьи',
                                                                    'h1' : 'Статьи на сайте'})




