import cgi



from controllers.controller import Controller
from models.user_auth_service import UserAuthService
from handlers import articles
from models.article import Article
from models.user import User
from exceptions import NotFoundException, UnauthorizedException, ForbiddenException, InvalidMethodException
from exceptions import InvalidArgumentException


class ArticlesController(Controller):
    def __init__(self, request):
        super().__init__(request)
        self.view.set_var(
            "csrf_token", UserAuthService.csrf_token_for_user(self.user)
        )

    def require_csrf_token(self, request):
        token = request.POST.get("csrf_token", "")
        if not UserAuthService.is_valid_csrf_token(self.user, token):
            raise ForbiddenException("Отсутствует или неверен CSRF-токен")

    def index(self, request, response):
        articles = Article.find_all()
        print(articles)
        response.text = self.view.render_html('articles/index.html', {'title' : 'Статьи',
                                                                      'h1' : 'Статьи на сайте',
                                                                      'articles' : articles,
                                                                      })

    def view(self, request, response, id):
        article = Article.get_by_id(id)
        if article is None:
            raise NotFoundException('Статья не найдена')

        user = User.get_by_id(article.get_author_id())
        response.text = self.view.render_html('articles/view.html', {'title' : f'MVC фреймворк - {article.get_name()}',
                                                                     'h1' : f'Статья: {article.get_name()} ',
                                                                     'article' : article,
                                                                     })


    def require_article_author(self, article):
        if self.user is None:
            raise UnauthorizedException('Необходимо авторизоваться')
        if str(article.get_author_id()) != str(self.user.get_id()):
            raise ForbiddenException('Нет прав на изменение чужой статьи')

    def edit(self, request, response, id):
        article = Article.get_by_id(id)
        if article is None:
            raise NotFoundException('Статья не найдена')

        self.require_article_author(article)

        if request.method == 'POST':
            self.require_csrf_token(request)
            article.set_name(request.POST['name'])
            article.set_text(request.POST['text'])
            article.save()
            response.status_code = 302
            response.headers = [('Location', f'/article/{article.get_id()}')]
            return

        response.text = self.view.render_html('articles/edit.html', {'title' : f'Редактирование  - {article.get_name()}', 'article' : article})


    def delete(self, request, response, id):
        if request.method != 'POST':
            raise InvalidMethodException('Удаление доступно только методом POST')
        article = Article.get_by_id(id)
        if article is None:
            raise NotFoundException('Статья не найдена')
        self.require_article_author(article)
        self.require_csrf_token(request)

        article.delete()
        response.status_code = 302
        response.headers = [('Location', '/articles')]



    def add(self, request, response):
        if self.user is None:
            raise UnauthorizedException("Необходимо авторизоваться")

        if request.method == "POST":
            self.require_csrf_token(request)
            form = request.POST
            fields = {
                "name": form.get("name", ""),
                "text": form.get("text", ""),
            }
            img_file = form.get("img")
            try:
                article = Article.create(fields, img_file, self.user)
                response.status_code = 302
                response.location = "/articles"
                return
            except InvalidArgumentException as exc:
                response.status_code = 400
                response.text = self.view.render_html(
                    "articles/add.html",
                    {"title": "Добавление статьи", "article_data": fields,
                     "error": exc},
                )
                return

        response.text = self.view.render_html(
            "articles/add.html", {"title": "Добавление статьи"}
        )
