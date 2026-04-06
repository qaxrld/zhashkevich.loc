from controllers.controller import Controller
from handlers import articles
from models.article import Article
from models.user import User
from exceptions import NotFoundException

class ArticlesController(Controller):

    def index(self, request, response):
        articles = Article.find_all()
        print(articles)
        response.text = self.view.render_html('articles/index.html', {'title' : 'Статьи',
                                                                    'h1' : 'Статьи на сайте', 'articles' : articles})

    def view(self, request, response, id):
        article = Article.get_by_id(id)
        if article is None:
            raise NotFoundException('Статья не найдена')

        user = User.get_by_id(article.get_author_id())
        response.text = self.view.render_html('articles/view.html', {'title' : f'MVC фреймворк - {article.get_name()}',
                                                                     'h1' : f'Статья: {article.get_name()} ',
                                                                     'article' : article,
                                                                     'user' : user})


    def edit(self, request, response, id):
        article = Article.get_by_id(id)
        if article is None:
            raise NotFoundException('Статья не найдена')




        if request.method == 'POST':
            article.set_name(request.POST['name'])
            article.set_text(request.POST['text'])
            article.save()
            response.status_code = 302
            response.headers = [('Location', f'/article/{article.get_id()}')]
            return

        response.text = self.view.render_html('articles/edit.html', {'title' : f'Редактирование  - {article.get_name()}', 'article' : article})


    def delete(self, request, response, id):
        article = Article.get_by_id(id)
        if article is None:
            raise NotFoundException('Статья не найдена')

        article.delete()
        response.status_code = 302
        response.headers = [('Location', '/articles')]



    def add(self, request,  response):
        article = Article()
        article.set_author_id(1)
        article.set_name('Новая статья')
        article.set_text('текст статьи')

        article.save()

