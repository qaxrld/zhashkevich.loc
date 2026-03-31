from controllers.controller import Controller
from models.article import Article

class ArticlesController(Controller):

    def index(self, request, response):
        articles = Article.find_all()
        print(articles)
        response.text = self.view.render_html('articles/index.html', {'title' : 'Статьи',
                                                                    'h1' : 'Статьи на сайте', 'articles' : articles})

    def view(self, request, response, id):
        article = Article.get_by_id(id)
        if article is None:
            response.status_code = 404
            response.text = self.view.render_html('errors/404.html', {'error' : 'Статья не найдена'})
            return

        response.text = self.view.render_html('articles/view.html', {'title' : f'MVC фреймворк - {article.get_name()}', 'h1' : f'Статья: {article.get_name()} ', 'article' : article})

    def edit(self, request, response, id):
        article = Article.get_by_id(id)
        if article is None:
            response.status_code = 404
            response.text = self.view.render_html('errors/404.html', {'error' : 'Статья не найдена'})
            return

        if request.method == 'POST':
            article.set_name(request.POST['name'])
            article.set_text(request.POST['text'])
            article.save()


        response.text = self.view.render_html('articles/edit.html', {'title' : f'Редактирование  - {article.get_name()}', 'article' : article})
